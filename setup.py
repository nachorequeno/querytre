from setuptools import find_packages, setup
from pybind11.setup_helpers import Pybind11Extension

libraries = ['gmp', 'gmpxx']

ext_instance_int = Pybind11Extension(
    'timedrel_ext_int',
    sources=['querytre/boost/timedrel_ext_int.cpp'],
    include_dirs=['include', '/usr/include'],
    cxx_std=11,
    # language = 'c++',
    libraries=libraries,
    library_dirs=['/usr/lib'],
)

ext_instance_float = Pybind11Extension(
    'timedrel_ext_float',
    sources=['querytre/boost/timedrel_ext_float.cpp'],
    include_dirs=['include', '/usr/include'],
    cxx_std=11,
    # language = 'c++',
    libraries=libraries,
    library_dirs=['/usr/lib'],
)

ext_instance_rational = Pybind11Extension(
    'timedrel_ext_rational',
    sources=['querytre/boost/timedrel_ext_rational.cpp'],
    include_dirs=['include', '/usr/include'],
    cxx_std=11,
    # language = 'c++',
    libraries=libraries,
    library_dirs=['/usr/lib', '/usr/lib/x86_64-linux-gnu'],
    extra_link_args=['-lgmp', '-lgmpxx'],
)

setup(
    name='querytre',
    packages=find_packages(),
    version='0.1.0',
    description='A library for querying Timed Regular Expressions (TRE)',
    author='Akshay Mambakam',
    license='GPLv3+',
    python_requires='>=3',
    install_requires=['antlr4-python3-runtime==4.7.1',
                      'pybind11>=2.11'],
    ext_package='timedrel',
    ext_modules=[ext_instance_int, ext_instance_float, ext_instance_rational]
)
