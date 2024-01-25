# from setuptools import setup
from distutils.core import setup

setup(
    packages=[
        'SambdaTester',
        'SambdaTester.modulator',
        'SambdaTester.yams',
        'SambdaTester.config'
        ],
    entry_points = {
        'console_scripts': [
            'SambdaTester=SambdaTester:main',
            'bin/SambdaTester=SambdaTester.command:main'
        ]
    },
    require=["pyyaml"],
    version="0.0.14",
    author_email = "tarnold0788@gmail.com"
)

# setup()