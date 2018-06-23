from booldog import compile_predicate

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
