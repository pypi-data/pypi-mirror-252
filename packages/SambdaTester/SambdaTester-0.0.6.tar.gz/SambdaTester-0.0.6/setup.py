from distutils.core import setup
from setuptools import find_packages

setup(
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'SambdaTester=SambdaTester:main',
            'bin/SambdaTester=SambdaTester.command:main'
        ]
    },
    version="0.0.6",
    author_email = "tarnold0788@gmail.com"
)
