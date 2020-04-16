import os
import sys

from Parser import Parser
from CodeWriter import CodeWriter
from Utils import *

def main():
    args = [x for x in sys.argv]

    if len(args) < 2:
        raise Exception("Error[7]: No file/dir name provided \"Usage: python VMTranslator.py file.vm\"")

    if not os.path.isfile(args[1]) and not os.path.isdir(args[1]):
        raise FileNotFoundError("Error[8]: \"" + args[1] + "\" does not exist")

    input_files = [args[1]]
    output_file_name = os.path.basename(os.path.abspath(args[1])).split(".")
    
    if len(output_file_name) > 1:
        output_file_name.pop()

    output_file_name = ".".join(output_file_name)

    if os.path.isdir(input_files[0]):
        input_files = [f for f in os.listdir(input_files[0]) if os.path.isfile(os.path.join(input_files[0], f))]
        input_files = [f for f in input_files if f.split(".")[-1] == "vm"]
        input_files = [os.path.abspath(f) for f in input_files]
        print(input_files)
        print(output_file_name)

    code_writer = CodeWriter(output_file_name)

    for file_name in input_files:
        parser = Parser(file_name)
        code_writer.setFileName(file_name)

        while parser.hasMoreCommands():
            parser.advance()
            arg1 = None
            arg2 = None

            if parser.commandType() != COMMAND_TYPES["C_RETURN"]:
                arg1 = parser.arg1()
            
            if parser.commandType() == COMMAND_TYPES["C_PUSH"] or \
                    parser.commandType() == COMMAND_TYPES["C_POP"] or \
                    parser.commandType() == COMMAND_TYPES["C_FUNCTION"] or \
                    parser.commandType() == COMMAND_TYPES["C_CALL"]:
                arg2 = parser.arg2()

            if parser.commandType() == COMMAND_TYPES["C_ARITHMETIC"] and arg1 is not None:
                code_writer.writeArithmetic(arg1)
            
            if (parser.commandType() == COMMAND_TYPES["C_PUSH"] or \
                    parser.commandType() == COMMAND_TYPES["C_POP"]) and \
                    arg1 is not None and arg2 is not None:
                code_writer.writePushPop(parser.commandType(), arg1, arg2)
        
    code_writer.close()

if __name__ == "__main__":
    main()
