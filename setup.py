from setuptools import setup

setup(
    name='markov-names',
    version='1.0.0',
    packages=['markov_names', 'markov_names.markov'],
    url='https://github.com/tristan-kreuziger/markov-names',
    license='MIT',
    author='Tristan Kreziger',
    author_email='.',
    description='This small tool allows to generate new names based on Markov chains after given an initial seed with some names. ',
    long_description=open('README.md').read()
)
