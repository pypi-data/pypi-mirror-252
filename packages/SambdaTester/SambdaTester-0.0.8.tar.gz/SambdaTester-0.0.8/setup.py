from setuptools import find_packages, setup

setup(
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'SambdaTester=SambdaTester:main',
            'bin/SambdaTester=SambdaTester.command:main'
        ]
    },
    version="0.0.8",
    author_email = "tarnold0788@gmail.com"
)
