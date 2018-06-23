import ast
import pytest

from boolcog.compiler import *


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
    func = compile_predicate(sexp, ['foo'])
    assert func(obj)

    foo = Foo()
    sexp = ['eq', ['identifier', 'bar'], foo]
    func = compile_predicate(sexp, ['bar'])
    assert func(foo)

    obj = [1, 2, 3]
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp, ['bar'])
    assert func(obj)

    obj = [Foo(), Foo(), Foo()]
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp, ['bar'])
    assert func(obj)

    obj = set([1, 2, 3])
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp, ['bar'])
    assert func(obj)

    obj = dict(a = 1, b = 2, c = 3)
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp, ['bar'])
    assert func(obj)

    obj = (1, 2, 3)
    sexp = ['eq', ['identifier', 'bar'], obj]
    func = compile_predicate(sexp, ['bar'])
    assert func(obj)