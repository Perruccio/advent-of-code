from setuptools import setup, find_packages

setup(
    name='advent-of-code',
    version='0.1.0',
    description='Solutions to Advent of Code',
    url='https://github.com/Perruccio/advent-of-code',
    author='Perruccio',
    author_email='',
    license='',
    packages=find_packages(),
    install_requires=['numpy', 'pytest'],

    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)