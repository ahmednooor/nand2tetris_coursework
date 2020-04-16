import os
import sys

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

def main():
    args = [x for x in sys.argv]

    if len(args) < 2:
        raise Exception("Error: No file/dir name provided \"Usage: python VMTranslator.py file.vm\"")

    if not os.path.isfile(args[1]) and not os.path.isdir(args[1]):
        raise FileNotFoundError("Error: \"" + args[1] + "\" does not exist")

    input_files = [os.path.abspath(args[1])]

    if os.path.isdir(input_files[0]):
        _input_files = [f for f in os.listdir(input_files[0])]
        _input_files = [f for f in _input_files if f.split(".")[-1] == "jack"]
        input_files = [os.path.join(input_files[0], f) for f in _input_files if f.split(".")[-1] == "jack"]

    for file_name in input_files:
        jackTokenizer = JackTokenizer(file_name)
        compilationEngine = CompilationEngine(jackTokenizer.tokens, file_name)


if __name__ == "__main__":
    main()