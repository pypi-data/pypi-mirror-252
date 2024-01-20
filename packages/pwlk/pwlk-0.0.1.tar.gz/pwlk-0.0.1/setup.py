from setuptools import setup

setup(
    name='pwlk',
    author='Loïc Pawlicki',
    version='0.0.1',
    install_requires=[
        'rich',
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
)