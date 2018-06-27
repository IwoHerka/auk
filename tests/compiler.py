import ast
import pytest
from types import FunctionType, LambdaType

from auk.compiler import *


class Foo(object):
    pass


def test_compile_terminal():
    assert type(compile_terminal(True, {})[0]) is ast.NameConstant
    assert type(compile_terminal(1, {})[0]) is ast.Num
    assert type(compile_terminal(1.0, {})[0]) is ast.Num
    assert type(compile_terminal(complex(1, 1), {})[0]) is ast.Num
    assert type(compile_terminal('str', {})[0]) is ast.Str
    assert type(compile_terminal(b'1', {})[0]) is ast.Bytes
    assert type(compile_terminal([], {})[0]) is ast.List
    assert type(compile_terminal(tuple(), {})[0]) is ast.Tuple
    assert type(compile_terminal({}, {})[0]) is ast.Dict
    assert type(compile_terminal(set(), {})[0]) is ast.Set

    scope = {}
    assert type(compile_terminal(object(), scope)[0]) is ast.Name
    assert scope

    scope = {}
    assert type(compile_terminal(Foo(), scope)[0]) is ast.Name
    assert scope


def test_defaults():
    sexp = ['tautology']
    assert type(compile_predicate(sexp)) is LambdaType
    sexp = ['eq', ['identifier', 'foo'], 1]
    assert type(compile_predicate(sexp)) is LambdaType
    sexp = ['eq', ['identifier', 'foo'], ['identifier', 'bar']]
    assert type(compile_predicate(sexp)) is FunctionType


def test_force():
    sexp = ['tautology']
    assert type(compile_predicate(sexp, force_func = True)) is FunctionType
    assert type(compile_predicate(sexp, force_lambda = True)) is LambdaType


def test_tautology():
    func = compile_predicate(['tautology'])
    assert func()
    with pytest.raises(TypeError):
        func(0)


def test_contradiction():
    func = compile_predicate(['contradiction'])
    assert not func()
    with pytest.raises(TypeError):
        func(0)


def test_object_literals():
    obj = object()
    sexp = ['eq', ['identifier', 'foo'], obj]
    func = compile_predicate(sexp)
    assert func(obj)

    foo = Foo()
    sexp = ['eq', ['identifier', 'bar'], foo]
    func = compile_predicate(sexp)
    assert func(foo)

    obj = [1, 2, 3]
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp)
    assert func(obj)

    obj = [Foo(), Foo(), Foo()]
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp)
    assert func(obj)

    obj = set([1, 2, 3])
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp)
    assert func(obj)

    obj = dict(a = 1, b = 2, c = 3)
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp)
    assert func(obj)

    obj = (1, 2, 3)
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp)
    assert func(obj)


def test_in():
    sexp = ['in', ['identifier', 'foo'], [1, 2, 3]]
    func = compile_predicate(sexp)
    assert func(foo = 1)
    assert not func(4)

    sexp = ['in', 1, [1, 2, 3]]
    func = compile_predicate(sexp)
    assert func()

    foo = object()
    sexp = ['in', foo, [foo, 2, 3]]
    func = compile_predicate(sexp)
    assert func()


def test_func():
    sexp = ['callable', lambda: True]
    func = compile_predicate(sexp)
    assert func()

    sexp = lambda: False
    func = compile_predicate(sexp)
    assert func()
