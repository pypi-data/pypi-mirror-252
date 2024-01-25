from distutils.core import setup

setup(
    packages=['SambdaTester'],
    entry_points = {
        'console_scripts': [
            'SambdaTester=SambdaTester:main',
            'bin/SambdaTester=SambdaTester.command:main'
        ]
    },
    version="0.0.5",
    author_email = "tarnold0788@gmail.com"
)
