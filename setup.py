from setuptools import find_packages, Extension, setup

ext_instance_int = Extension(
    'ext_int',
    sources=['timedrel/boost/timedrel_ext_int.cpp'],
    include_dirs=['include'],
    libraries=['boost_python3'],
)

ext_instance_float = Extension(
    'ext_float',
    sources=['timedrel/boost/timedrel_ext_float.cpp'],
    include_dirs=['include'],
    libraries=['boost_python3'],
)

setup(
    name='querytre',
    packages=find_packages(),
    version='0.1.0',
    description='A library for querying Timed Regular Expressions (TRE)',
    author='Akshay Mambakam',
    license='GPLv3+',
    python_requires='>=3',
    install_requires=['antlr4-python3-runtime>=4.13'],
    ext_package='timedrel',
    ext_modules=[ext_instance_int, ext_instance_float]
)