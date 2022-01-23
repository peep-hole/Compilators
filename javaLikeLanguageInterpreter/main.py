from myParser import Parser
from myInterpreter import Interpreter
import sys
import ply.yacc as yacc

if __name__ == '__main__':
    try:
        filename = "example2.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open example.txt file")
        sys.exit(0)

    parser = Parser()
    pars = yacc.yacc(module=parser)
    content = file.read()

    tree = pars.parse(content, lexer=parser.scanner)

    interpret = Interpreter()
    tree.accept(interpret)

