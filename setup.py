from setuptools import setup

setup(
    name='simulator',
    version='1.0',
    description='A tomasulo simulator module',
    author='Daniel Stumpp, Colman Glagovich, Owen Lucas',
    author_email='dcs98@pitt.edu',
    packages=['simulator'],  # same as name
    # external packages as dependencies
    install_requires=['pytest', 'pytest-cov', 'coveralls','pyyaml'],
)
