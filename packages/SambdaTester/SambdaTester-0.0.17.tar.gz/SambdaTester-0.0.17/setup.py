# from setuptools import setup
from distutils.core import setup

setup(
    packages=[
        'SambdaTester',
        'SambdaTester.modulator',
        'SambdaTester.yams',
        'SambdaTester.yams.models',
        'SambdaTester.config',
        'SambdaTester.server'
        ],
    entry_points = {
        'console_scripts': [
            'SambdaTester=SambdaTester:main',
            'bin/SambdaTester=SambdaTester.command:main'
        ]
    },
    require=[
        "pyyaml",
        "pydantic",
        "python-dotenv"
        ],
    version="0.0.17",
    author_email = "tarnold0788@gmail.com"
)

# setup()