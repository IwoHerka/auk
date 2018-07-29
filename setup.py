from setuptools import setup

setup(
    name             = 'auk',
    version          = '0.1.1',
    license          = 'MIT',
    requires         = ['python (>= 3.4)'],
    provides         = ['auk'],
    description      = 'Micro-package for compiling s-expressions into Python\'s predicate functions' ,
    url              = 'http://github.com/IwoHerka/auk',
    packages         = ['auk', 'tests'],
    maintainer       = 'Iwo Herka',
    maintainer_email = 'hi@iwoherka.eu',
    author           = 'Iwo Herka',
    author_email     = 'hi@iwoherka.eu',

    include_package_data = True,
    package_data = dict(auk = ['*.yml']),
    package_dir = dict(auk = 'auk'),
    install_requires = [
        'sexpr'
    ],

    classifiers  = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python'
    ],
)
