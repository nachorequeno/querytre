# QueryTRE
QueryTRE is a fork of [Timedrel] and [Montre] that exports Timed Regular Expressions to [ParetoLib].

[Timedrel]: https://github.com/doganulus/timedrel
[Montre]: https://github.com/doganulus/montre
[ParetoLib]: https://gricad-gitlab.univ-grenoble-alpes.fr/verimag/tempo/multidimensional_search

# Installation
In order to install QueryTRE, run the following commands:

``
pip3 install .
``

Alternatively, you can compile and pack the library into a *.whl file.

``
python3 setup.py bdist_wheel --universlal --force-reinstall
pip3 install ./dist/querytre-0.1.0-py3-none-any.whl 
``

Then, you can install the *.whl file using the installation procedure for Python libraries.

**Remark**: On Linux/macOS you will probably need g++.

# Dependencies: Antlr4
Lexer and parser.py files in **querytre/parser** folder are automatically generated using Antlr4 (version 4.7.13). 
In order to correctly import this module in Python, you must install the exact version it was compiled for:

``
user@localhost:~/pip install antlr4-python3-runtime==4.7.13
``

Alternatively, you can recompile the **querytre/parser** folder. To do so, you must download the Antlr4 jar file from the official website, and execute:

``
user@localhost:~/querytre/querytre/parser$ java -jar antlr-4.7.13-complete.jar *.g4 -Dlanguage=Python3
``