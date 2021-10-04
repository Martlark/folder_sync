from setuptools import setup

setup(
    name='folder_sync',
    version='0.4.0',
    py_modules=['folder_sync'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'folder_sync = folder_sync:cli',
        ],
    },
)