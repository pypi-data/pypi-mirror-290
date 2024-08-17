from setuptools import setup

setup(
    name='pyclasses',
    version='0.3',
    py_modules=['pyclasses'],
    install_requires=[
        "pydot",
        "setuptools"
    ],
    entry_points={
        'console_scripts': [
            'pyclasses=pyclasses:main',
        ],
    },
)