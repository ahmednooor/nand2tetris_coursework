import os
import sys

from CodeWriter import CodeWriter
from Parser import Parser
# from Utils import *

def main():
    args = [x for x in sys.argv]

    if len(args) < 2:
        raise Exception("Error[7]: No file/dir name provided \"Usage: python VMTranslator.py file.vm\"")

    if not os.path.isfile(args[1]) and not os.path.isdir(args[1]):
        raise FileNotFoundError("Error[8]: \"" + args[1] + "\" does not exist")

    input_files = [os.path.abspath(args[1])]
    print(input_files)
    output_file_name = os.path.abspath(args[1])
    is_input_dir = False

    if os.path.isdir(input_files[0]):
        is_input_dir = True
        input_files = [f for f in os.listdir(input_files[0])]
        input_files = [f for f in input_files if f.split(".")[-1] == "asm"]
        input_files = [os.path.join(output_file_name, f) for f in input_files]
        output_file_name = os.path.join(output_file_name, os.path.basename(output_file_name))
        print(input_files)
        print(output_file_name)

    for file_name in input_files:
        parser = Parser(file_name)
        codeWriter = CodeWriter(file_name, parser.tokens, parser.symbol_table)

if __name__ == "__main__":
    main()
