# Antlr4
Lexer and parser.py files in **querytre/parser** folder are automatically generated using Antlr4 (version 4.7.13). 
In order to correctly import this module in Python, you must install the exact version it was compiled for:

``
user@localhost:~/pip install antlr4-python3-runtime==4.7.13
``

Alternatively, you can recompile the **querytre/parser** folder. To do so, you must download the Antlr4 jar file from the official website, and execute:

``
user@localhost:~/querytre/querytre/parser$ java -jar antlr-4.7.13-complete.jar *.g4 -Dlanguage=Python3
``