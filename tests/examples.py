from auk import compile_predicate


def test_example_1():
    sexp = \
        ['not',
            ['and',
                ['tautology'],
                ['eq',
                    ['identifier', 'lucky_number'],
                    777
                ]
            ]
        ]

    func = compile_predicate(sexp)
    assert not func(777)
    assert func(7)


def test_example_2():
    P, Q = True, False

    sexp = \
        ['not',
            ['or',
                ['identifier', 'P'],
                ['identifier', 'Q'],
            ]
        ]

    func = compile_predicate(sexp)
    assert func(P, Q) == (not P and not Q)

def test_example_3():
    # num in [1, 2, 3] and num >= 2

    sexp = \
        ['and',
            ['in', ['identifier', 'num'], [1, 2, 3]],
            ['gte', ['identifier', 'num'], 2]
        ]

    func = compile_predicate(sexp)
    assert not func(1)
    assert func(2)
    assert func(3)

