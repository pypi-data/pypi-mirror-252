# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import sys
import time
import typing
import unicodedata

import cv2
import cv2.aruco
import matplotlib.path
import matplotlib.transforms
import numpy as np

from loguru import logger

from . import (
    ast,
    blocks,
)

class Affine2DWithAxisRotation(matplotlib.transforms.Affine2D):
    def rotate_to_axis(self, axis_unit_vector):
        vx, vy = axis_unit_vector
        rotate_mtx = np.array([
            [-vy,  vx,   0],
            [-vx, -vy,   0],
            [  0,   0,   1]], float)
        self._mtx = rotate_mtx @ self._mtx
        self.invalidate()
        return self

    def rotate_from_axis(self, axis_unit_vector):
        vx, vy = axis_unit_vector
        rotate_mtx = np.array([
            [-vy, -vx,   0],
            [ vx, -vy,   0],
            [  0,   0,   1]], float)
        self._mtx = rotate_mtx @ self._mtx
        self.invalidate()
        return self

def draw_label(img, text, org, fontFace, fontScale, color_bg, color_fg, thickness):
    if img is None:
        return None
    text = text.replace('Ł', 'L').replace('ł', 'l')
    text = ''.join(c for c in unicodedata.normalize('NFKD', text)
        if unicodedata.category(c)[0] != 'M')
    textsize, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    cv2.rectangle(
        img,
        (org[0] - 2, org[1] + baseline + 2),
        (org[0] + textsize[0] + 2, org[1] - textsize[1] - baseline - 2),
        color_bg,
        -1,
    )
    cv2.putText(img, text, org, fontFace, fontScale, color_fg, thickness)
    return img

def draw_path(img, path, color, thickness):
    if img is None:
        return None
    cv2.polylines(
        img, np.array(path.to_polygons()).astype(int), True, color, thickness)
    return img

class Detection(typing.NamedTuple):
    aruco_id: int
    corners: np.ndarray
    block: blocks.Block

    def _debug_draw(self, frame, corners, color_bg, color_fg):
        if frame is None:
            return

        cv2.polylines(frame, corners.reshape((1,4,2)).astype(int), True,
                color_bg, 2)

        top_left, *_ = corners
        cv2.rectangle(
            frame,
            top_left - [5, 5],
            top_left + [5, 5],
            color_bg,
            thickness=-1,
        )
        draw_label(
            frame,
            f'{self.aruco_id} ({self.block})',
            (top_left[0] + 10, top_left[1] + 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color_bg,
            color_fg,
            2,
        )

    def debug_draw(self, frame, color_bg=(0, 0, 0), color_fg=(255, 255, 255)):
        return self._debug_draw(frame, self.corners, color_bg, color_fg)

    def debug_draw_flipped(self, frame, color_bg=(0, 0, 0), color_fg=(255, 255, 255)):
        _, width, _ = frame.shape
        return self._debug_draw(frame, np.array([
            (width - x, y) for x, y in self.corners
        ]))

    def get_next_detect_areas(
        self, base_transform, axis_v, axis_h, *, debug_frame=None,
    ):
        top_left, _, _, bottom_left = self.corners
        marker_height = np.linalg.norm(top_left - bottom_left)
        corners_path = matplotlib.path.Path(self.corners)

        transform = (
              matplotlib.transforms.Affine2D()
                .translate(*-top_left)
            + base_transform
            + matplotlib.transforms.Affine2D()
                .translate(*top_left)
                .translate(*axis_v * marker_height * -0.6)
        )
        transform_v = (transform + matplotlib.transforms.Affine2D()
            .translate(*axis_v * marker_height * 2.2)
            .translate(*axis_h * marker_height * -1))

        transform_h = (transform + matplotlib.transforms.Affine2D()
            .translate(*axis_h * marker_height * 4.5)
        )

        next_area_v = transform_v.transform_path(corners_path)
        next_area_h = transform_h.transform_path(corners_path)

        return next_area_v, next_area_h


class Detector:
    def __init__(self, blur=1):
        self.blocks = blocks.BlockLoader()
        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_ARUCO_ORIGINAL)
        self.blur = blur
#       self.parameters = cv2.aruco.DetectorParameters_create()
#       self.parameters.detectInvertedMarker = True

    def detect_markers(self, frame):
        start_time = time.perf_counter()
        frame = 255 - frame
        if self.blur > 1:
            frame = cv2.blur(frame, (self.blur, self.blur))

        corners, ids, _rejected = cv2.aruco.detectMarkers(
            image=frame,
            dictionary=self.dictionary,
#           parameters=self.parameters,
        )

#       logger.debug(f'{rejected=}')

        if ids is not None:
            for c, aruco_id in zip(corners, ids.flatten()):
                try:
                    block = self.blocks.get_block_by_aruco_id(aruco_id)
                except LookupError:
                    block = None
                yield Detection(aruco_id, c.reshape((4, 2)).astype(int), block)

        perf_ms = (time.perf_counter() - start_time) * 1000
#       logger.debug(f'detect_markers() took {perf_ms:.3f} ms')

class BoardError(Exception):
    pass

class Analyser:
    def __init__(self, detections):
        self.detections = list(detections)

    def find_start_and_end(self):
        start = None
        end = None
        is_func = None

        for i in range(len(self.detections)-1, -1, -1):
            block = self.detections[i].block
            if block is None:
                continue
            token = block.token
#           logger.debug(f'{token=} {start=} {end=}')
            if token.type in (blocks.TokenType.BEGIN, blocks.TokenType.END):
                if token.type is blocks.TokenType.BEGIN:
                    if start is not None:
                        raise BoardError('double start tile')
                    start = self.detections[i]
                else:
                    if end is not None:
                        raise BoardError('double end tile')
                    end = self.detections[i]
                current_is_func = token in (blocks.Token.DEFINE_FUNCTION,
                        blocks.Token.END_FUNCTION)
                if is_func is not None and current_is_func != is_func:
                    raise BoardError('mismatched start and end')
                is_func = current_is_func
                del self.detections[i]

        if start is None:
            raise BoardError('no start tile')
        if end is None:
            raise BoardError('no start tile')

        return start, end

    def find_detection_in_area(self, area, *, debug_frame=None):
        """
        Find a single `Detection` inside *area* given by `matplotlib.path.Path`

        If there aren't any, return `None`. If there are more than one, raises
        `BoardError`.

        Any detections found are removed from self.detections.

        Debug drawing:

        - on found or `None`, draws cyan area and white-on-black detection
        - on error, draws red area and white-on-red detection
        """
        candidate = None
        found_multiple = False
        for i in range(len(self.detections)-1, -1, -1):
            i_top_left, *_ = self.detections[i].corners
            if area.contains_point(i_top_left):
                if found_multiple or candidate is not None:
                    found_multiple = True
                    self.detections.pop(i).debug_draw(debug_frame, (0, 0, 255))
                    continue

                candidate = self.detections.pop(i)

        if found_multiple:
            candidate.debug_draw(debug_frame, (0, 0, 255))
            draw_path(debug_frame, area, (0, 0, 255), 2)
            raise BoardError('more than one candidate in detection area')

        if candidate is not None:
            candidate.debug_draw(debug_frame)
        draw_path(debug_frame, area, (255, 255, 0), 2)
        return candidate

    def get_line(
        self, detection, area_h, base_transform, axis_v, axis_h, *,
        debug_frame=None
    ):
        while True:
            yield detection.block.token
            detection = self.find_detection_in_area(area_h,
                debug_frame=debug_frame)
            if detection is None:
                break
            _, area_h = detection.get_next_detect_areas(
                base_transform, axis_v, axis_h, debug_frame=debug_frame)

    def get_programme(self, *, debug_frame=None):
        start_time = time.perf_counter()

        # 1. find start and end tiles
        start, end = self.find_start_and_end()

        # 2. calculate main axis and unit vector parallel to axis
        start_top_left, *_ = start.corners
        end_top_left, *_ = end.corners

        if debug_frame is not None:
#           cv2.line(debug_frame, start_top_left, (0, 0), (255, 255, 0), 2)
            cv2.line(debug_frame, start_top_left, end_top_left, (255, 255, 0), 2)

        axis = end_top_left - start_top_left
        axis_v = axis / np.linalg.norm(axis)
        axis_h = np.array([axis_v[1], -axis_v[0]])

        # 3. calcucate transforms for rotating and scaling detection area
        # (will be applied to each marker outline around its top_left)
        # (will be used for both horizontal and vertical areas)
        base_transform = (Affine2DWithAxisRotation()
            .rotate_to_axis(axis_v)
            # 4 == difference between narrowest and widest tile + 1
            .scale(4, 1.2)
            .rotate_from_axis(axis_v)
        )

        # 4. yield all the lines
        try:
            current = start
            while True:
                detect_area_v, detect_area_h = current.get_next_detect_areas(
                    base_transform, axis_v, axis_h, debug_frame=debug_frame)
                yield tuple(self.get_line(current, detect_area_h,
                    base_transform, axis_v, axis_h, debug_frame=debug_frame))

                if detect_area_v.contains_point(end_top_left):
                    yield (end.block.token,)
                    if debug_frame is not None:
                        end.debug_draw(debug_frame)
                    break

                current = self.find_detection_in_area(detect_area_v,
                    debug_frame=debug_frame)

                if current is None:
                    raise BoardError('no candidate in detection area')

        finally:
            if debug_frame is not None:
                for detection in self.detections:
                    detection.debug_draw(debug_frame, color_bg=(0, 255, 255),
                            color_fg=(0, 0, 0))

        perf_ms = (time.perf_counter() - start_time) * 1000
#       logger.debug(f'get_programme() took {perf_ms:.3f} ms')

# vim: tw=80 ts=4 sts=4 sw=4 et
