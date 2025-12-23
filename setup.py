from setuptools import setup, find_packages

setup(
    name='aoc',
    version='0.1.0',
    description='Solutions to Advent of Code',
    url='https://github.com/Perruccio/advent-of-code',
    author='Perruccio',
    author_email='',
    license='',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=['numpy', 'pytest', 'sympy', 'networkx', 'scipy'],

    classifiers=[
        'Programming Language :: Python :: 3.11'
    ],
    python_requires=">=3.11",

)