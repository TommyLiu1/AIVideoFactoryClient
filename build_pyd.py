from setuptools import setup
from Cython.Build import cythonize

setup(
    name='一个名字',
    ext_modules=cythonize(
        [
            "app_main.py",
            "ui/*.py",
            "utils/*.py",
            "api/*.py"
        ],
        language_level=3
    ),
)