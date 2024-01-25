from distutils.core import setup

setup(
    packages=['SambdaTester'],
    entry_points = {
        'console_scripts': [
            'DoItLive=SambdaTester:main',
            'bin/DoItLive=DoItLive.command:main'
        ]
    },
    version="0.0.2",
    author_email = "tarnold0788@gmail.com"
)
