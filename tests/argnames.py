from auk.compiler import read_argnames

def test_read_argnames():
    sexp = ['eq', ['identifier', 'bar'], True]
    argnames = read_argnames(sexp)
    assert argnames == set(['bar'])

    sexp = ['eq', ['identifier', 'bar'], ['identifier', 'foo']]
    argnames = read_argnames(sexp)
    assert argnames == set(['bar', 'foo'])

    sexp = \
        ['not',
            ['and',
                ['identifier', 'arg1'],
                ['eq',
                    ['identifier', 'arg2'],
                    ['identifier', 'arg3']
                ]
            ],
            ['not', ['identifier', 'arg4']]
        ]

    argnames = read_argnames(sexp)
    assert argnames == set(['arg1', 'arg2', 'arg3', 'arg4'])
