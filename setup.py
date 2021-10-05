from setuptools import setup

setup(
    name='py_sync',
    version='1.0.0',
    py_modules=['py_sync'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'py_sync = py_sync:cli',
        ],
    },
)