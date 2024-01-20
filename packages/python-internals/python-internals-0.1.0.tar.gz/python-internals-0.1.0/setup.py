from setuptools import setup, Extension
from sysconfig import get_config_var

python_include = get_config_var('INCLUDEPY')

setup(
    name="python-internals",
    version="0.1.0",
    ext_modules=[
        Extension(
            'internals',
            ['c/internals.c'],
            include_dirs=[python_include],
            extra_compile_args=["-O3"]
        )
    ]
)
