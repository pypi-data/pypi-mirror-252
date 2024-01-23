# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import operator
from dataclasses import dataclass

from funcparserlib import parser as _parser

from . import (
    ast,
    blocks,
)

@dataclass(frozen=True)
class ParseToken:
    token: blocks.Token
    line: int
    col: int

    @classmethod
    def stream_from_lines(cls, lines):
        for lineno, line in enumerate(lines, start=1):
            i = 1
            for token in line:
                yield cls(token, lineno, i)
                i += 1
            yield cls(blocks.Token.NEWLINE, lineno, i)

def _line_cols(*parsed):
    lineset = {t.line for t in parsed if t is not None}
    line = lineset.pop()
    assert not lineset

    colset = set()
    for t in parsed:
        if isinstance(t, ast.Parsed):
            colset.update(t.cols)
        elif isinstance(t, ParseToken):
            colset.add(t.col)
        else:
            assert t is None
    return line, (min(colset), max(colset))

# make_ functions

def make_Number(parsed):
    sign_minus, digits = parsed
    return ast.Number(*_line_cols(sign_minus, *digits),
        int(''.join(d.token.text for d in digits))
        * (-1 if sign_minus is not None else 1))

def make_Variable(parsed):
    return ast.Variable(*_line_cols(parsed), parsed.token.text)

def make_Forever(parsed):
    return ast.Forever(*_line_cols(parsed))

def make_Assign(parsed):
    start, var, exp = parsed
    return ast.Assign(*_line_cols(*parsed), var.token.text, exp)

_ops = {
    blocks.Token.PLUS: operator.add,
    blocks.Token.MINUS: operator.sub,
}
def make_BinOp(parsed):
    first, rest = parsed
    left = first
    for o, right in rest:
        left = ast.BinOp(_line_cols(left, o, *right), _ops[o], left, right)
    return left

def make_Condition(parsed):
    d, o = parsed
    return ast.Condition(*_line_cols(*parsed),
        ast.Direction(d.token.text), ast.Object(o.token.text))

def make_Function(parsed):
    start, funcname, funcbody, end = parsed
    return ast.Function(*cls._line_cols(start, funcname), (start.line, end.line),
        funcbody, funcname.token.value)

def make_Repeat(parsed):
    start, counter, body, end = parsed
    return ast.Repeat(*_line_cols(start, counter), (start.line, end.line),
        body, counter)

def make_If(parsed):
    start, condition, body, orelse = parsed
    if isinstance(orelse, ParseToken) and orelse.token == blocks.Token.END_BLOCK:
        lines = (start.line, orelse.line)
        orelse = None
    else: # If or Else
        lines = (start.line, orelse.lines[1])
    return ast.If(*_line_cols(start, condition), lines,
        body, condition, orelse)

def make_RepeatWhile(parsed):
    start, cond, body, end = parsed
    return ast.RepeatWhile(*_line_cols(start, cond), (start.line, end.line),
        body, cond)

def make_simple(cls):
    def make_simple(parsed):
        if isinstance(parsed, ParseToken):
            parsed = [parsed]
        return cls(*_line_cols(*parsed), *parsed[1:])
    return make_simple

def make_CallFunction(parsed):
    start, funcname = parsed
    return ast.CallFunction(*_line_cols(*parsed), funcname.token.text)

def make_block(cls):
    def make_block(parsed):
        start, body, end = parsed
        return cls(*_line_cols(start), (start.line, end.line), body)
    return make_block


# helper parsers

def tok(token):
    return _parser.some(lambda t: t.token == token).named(token.name)

def toktype(type):
    return _parser.some(lambda t: t.token.type == type).named(type)

def toktype_(type):
    return _parser.skip(toktype(type))

def name(parsed):
    return parsed.token.value

# grammar

newline = toktype_(blocks.TokenType.NEWLINE)

digit = toktype(blocks.TokenType.DIGIT)
varname = toktype(blocks.TokenType.VARNAME)
funcname = toktype(blocks.TokenType.FUNCNAME)
op = toktype(blocks.TokenType.OP)
direction = toktype(blocks.TokenType.DIRECTION)
obj = toktype(blocks.TokenType.OBJECT)

minus = tok(blocks.Token.MINUS)
equals = _parser.skip(tok(blocks.Token.EQUALS))

number = (_parser.maybe(minus) + _parser.oneplus(digit)
    ).named('number') >> make_Number
term = number | varname
expr = (term + _parser.many(op + term)).named('expr') >> make_BinOp
forever = tok(blocks.Token.FOREVER) >> make_Forever

condition = (direction + obj).named('condition') >> make_Condition

statement = _parser.forward_decl().named('statement')
body = _parser.many(statement).named('body')
end_block = tok(blocks.Token.END_BLOCK)

simple_stmt = (
    tok(blocks.Token.TURN_LEFT) >>      make_simple(ast.TurnLeft) |
    tok(blocks.Token.TURN_RIGHT) >>     make_simple(ast.TurnRight) |
    tok(blocks.Token.JUMP) >>           make_simple(ast.Jump) |
    tok(blocks.Token.PICK_UP) >>        make_simple(ast.PickUp) |
    tok(blocks.Token.ACTIVATE) >>       make_simple(ast.Activate) |
    tok(blocks.Token.DRAW) >>           make_simple(ast.Draw) |
    tok(blocks.Token.BREAK) >>          make_simple(ast.Break) |
    tok(blocks.Token.BREAK_FUNCTION) >> make_simple(ast.BreakFunction) |

    (tok(blocks.Token.STEP) + expr)
        >> make_simple(ast.Step) |
    (tok(blocks.Token.PLACE) + direction)
        >> make_simple(ast.Place) |
    (tok(blocks.Token.VARIABLE) + varname + equals + expr)
        >> make_simple(ast.Assign) |

    (tok(blocks.Token.CALL_FUNCTION) + funcname)
        >> make_CallFunction
) + newline

repeat_stmt = (
    tok(blocks.Token.REPEAT) + (forever | expr) + newline +
    body +
    end_block + newline
) >> make_Repeat

repeat_while_stmt = (
    tok(blocks.Token.REPEAT_WHILE) + condition + newline +
    body +
    end_block + newline
) >> make_RepeatWhile

else_stmt = (
    tok(blocks.Token.ELSE) + newline +
    body +
    end_block + newline
) >> make_block(ast.Else)

elif_stmt = _parser.forward_decl()
elif_stmt.define(
    tok(blocks.Token.ELSE_IF) + condition + newline +
    body +
    (elif_stmt >> make_If | else_stmt | end_block + newline)
)

if_stmt = (
    tok(blocks.Token.IF) + condition + newline +
    body +
    (elif_stmt >> make_If | else_stmt | end_block + newline)
) >> make_If

statement.define(
    simple_stmt |
    repeat_stmt |
    repeat_while_stmt |
    if_stmt
)

programme = (
    (tok(blocks.Token.BEGIN) + newline).named('begin') +
    body +
    (tok(blocks.Token.END) + newline).named('end') +
    _parser.skip(_parser.finished)
) >> make_block(ast.Programme)

function = (
    (tok(blocks.Token.DEFINE_FUNCTION) + funcname + newline).named('define') +
    body +
    (tok(blocks.Token.END_FUNCTION) + newline).named('endfunc') +
    _parser.skip(_parser.finished)
)

parser = programme | function

def parse(lines):
    return parser.parse(list(ParseToken.stream_from_lines(lines)))

# vim: tw=80 ts=4 sts=4 sw=4 et
