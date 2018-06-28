"""
    nodes
    ~~~~~

    Contains compilation function for each valid tag in the grammar.
    For example, 'and' is compiled to `ast.BoolOp` with "op" equal to 
    `ast.And()`.
"""
import ast
from typing import Any


def compile_comparison(first: Any, second: Any, opnode: ast.AST) -> ast.Compare:
    return ast.Compare(
        ops = [opnode()],
        left = first,
        comparators = [second]
    )

def compile_eq(first, second):
    return compile_comparison(first, second, ast.Eq)

def compile_neq(first, second):
    return compile_comparison(first, second, ast.NotEq)

def compile_lt(first, second):
    return compile_comparison(first, second, ast.Lt)

def compile_lte(first, second):
    return compile_comparison(first, second, ast.LtE)

def compile_gt(first, second):
    return compile_comparison(first, second, ast.Gt)

def compile_gte(first, second):
    return compile_comparison(first, second, ast.GtE)

def compile_in(first, second):
    return compile_comparison(first, second, ast.In)

def compile_identifier(name):
    return ast.Name(id = name, ctx = ast.Load())

def compile_tautology():
    return ast.NameConstant(value = True)

def compile_contradiction():
    return ast.NameConstant(value = False)

def compile_not(operand):
    return ast.UnaryOp(op = ast.Not(), operand = operand)

def compile_and(*values):
    return ast.BoolOp(op = ast.And(), values = list(values))

def compile_or(*values):
    return ast.BoolOp(op = ast.Or(), values = list(values))

def compile_callable(func):
    return ast.Call(func = func, args = [], keywords = [])
