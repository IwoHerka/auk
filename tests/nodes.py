import ast

from auk.nodes import *


def test_compile_and():
    body = [object(), object()]
    tree = compile_and(*body)
    assert type(tree) is ast.BoolOp
    assert type(tree.op) is ast.And
    assert tree.values == body

def test_compile_or():
    body = [object(), object()]
    tree = compile_or(*body)
    assert type(tree) is ast.BoolOp
    assert type(tree.op) is ast.Or
    assert tree.values == body

def test_compile_not():
    operand = object()
    tree = compile_not(operand)
    assert type(tree) is ast.UnaryOp
    assert type(tree.op) is ast.Not
    assert tree.operand is operand

def test_compile_tautology():
    tree = compile_tautology()
    assert type(tree) is ast.NameConstant
    assert tree.value is True

def test_compile_contradiction():
    tree = compile_contradiction()
    assert type(tree) is ast.NameConstant
    assert tree.value is False

def test_compile_identifier():
    name = object()
    tree = compile_identifier(name)
    assert tree.id is name
    assert type(tree.ctx) is ast.Load

def test_comparisons():
    def test_comparison(compile_func, opcls):
        first, second = object(), object()
        tree = compile_func(first, second)
        assert type(tree) is ast.Compare
        assert type(tree.ops[0]) is opcls
        assert tree.left is first
        assert tree.comparators == [second]

    test_comparison(compile_eq, ast.Eq)
    test_comparison(compile_neq, ast.NotEq)
    test_comparison(compile_lt, ast.Lt)
    test_comparison(compile_lte, ast.LtE)
    test_comparison(compile_gte, ast.GtE)
    test_comparison(compile_in, ast.In)
