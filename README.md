# QueryTRE
QueryTRE is a fork of [Timedrel] and [Montre] that exports Timed Regular Expressions to [ParetoLib].
It supports the analysis of TRE with time intervals in integer/floating-point/rational numbers. 
It also supports advanced features such as trace diagnostics (i.e., decomposition of traces into fragments of satisfaction/falsification intervals).

[Timedrel]: https://github.com/doganulus/timedrel
[Montre]: https://github.com/doganulus/montre
[ParetoLib]: https://gricad-gitlab.univ-grenoble-alpes.fr/verimag/tempo/multidimensional_search

# Installation
In order to install QueryTRE, run the following commands:

``
pip3 install .
``

# Compilation
Alternatively, you can compile and pack the library into a *.whl file.

``
python3 setup.py bdist_wheel --universal
``

``
pip3 install  --force-reinstall ./dist/querytre-0.1.0-py3-none-any.whl 
``

Then, you can install the *.whl file using the installation procedure for Python libraries.

**Remark**: On Linux/macOS you will probably need g++.

# Dependencies: 
## GMP and PPL
QueryTRE uses **Parma Polyhedra Library (PPL)** for implementing the algorithms for TRE evaluation and diagnostics. 
PPL depends on the **GNU Multiple Precision (GMP) Arithmetic Library**.
Additionally, we use **pybind11** to create **Python3** bindings.
You must install both libraries before installing QueryTRE.
On Ubuntu, you can install them running:
We provide a list of detailed commands for Ubuntu.

1. Install Parma Polyhedra Library (PPL).
```
sudo apt install ppl-dev
```
2. Install C++ compiler.
```
sudo apt install g++
```
3. Install the GNU Multiple Precision (GMP) Arithmetic Library.
```
sudo apt install libgmp-dev
```
4. Install
```
./build.sh
```
5. Run
```
python3 ./examples/robustness_example_1.py
```


## Antlr4
Lexer and parser.py files in **querytre/parser** folder are automatically generated using Antlr4 (version 4.7.13). 
In order to correctly import this module in Python, you must install the exact version it was compiled for:

``
user@localhost:~/pip install antlr4-python3-runtime==4.7.13
``

Alternatively, you can recompile the **querytre/parser** folder. To do so, you must download the Antlr4 jar file from the official website, and execute:

``
user@localhost:~/querytre/querytre/parser$ java -jar antlr-4.7.13-complete.jar *.g4 -Dlanguage=Python3
``

# Authors and acknowledgment
This package is built on top of the work done at the VERIMAG laboratory located in the Grenoble city of France. This work is based on the theory of timed pattern matching developed by Dogan Ulus. Check out his [github page](https://github.com/doganulus).

# License
For open source projects, say how it is licensed.