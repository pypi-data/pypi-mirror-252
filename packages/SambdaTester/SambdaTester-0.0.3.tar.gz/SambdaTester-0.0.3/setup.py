from distutils.core import setup

setup(
    packages=['SambdaTester'],
    entry_points = {
        'console_scripts': [
            'DoItLive=SambdaTester:main',
            'bin/DoItLive=SambdaTester.command:main'
        ]
    },
    version="0.0.3",
    author_email = "tarnold0788@gmail.com"
)
