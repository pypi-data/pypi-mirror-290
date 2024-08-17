from setuptools import setup

setup(
    name='pyclasses',
    version='0.2',
    py_modules=['pyclasses'],
    install_requires=[
        "pydot",
        "setuptools"
    ],
    entry_points={
        'console_scripts': [
            'pyclasses=pyclasses:main',  # 'my_command' 是在命令行中调用的命令，'pyclasses:main' 表示 pyclasses.py 中的 main 函数
        ],
    },
)