import os
import sys

from CodeWriter import CodeWriter
from Parser import Parser
from Utils import *

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
        input_files = [f for f in input_files if f.split(".")[-1] == "vm"]
        input_files = [os.path.join(output_file_name, f) for f in input_files]
        output_file_name = os.path.join(output_file_name, os.path.basename(output_file_name))
        print(input_files)
        print(output_file_name)

    code_writer = CodeWriter(output_file_name)
    if is_input_dir:
        code_writer.writeInit()

    for file_name in input_files:
        parser = Parser(file_name)
        code_writer.setFileName(file_name)


        while parser.hasMoreCommands():
            parser.advance()
            arg1 = None
            arg2 = None

            if parser.commandType() != CommandTypes.C_RETURN:
                arg1 = parser.arg1()
            
            if parser.commandType() == CommandTypes.C_PUSH or \
                    parser.commandType() == CommandTypes.C_POP or \
                    parser.commandType() == CommandTypes.C_FUNCTION or \
                    parser.commandType() == CommandTypes.C_CALL:
                arg2 = parser.arg2()

            if parser.commandType() == CommandTypes.C_ARITHMETIC and arg1 is not None:
                code_writer.writeArithmetic(arg1)
            
            if (parser.commandType() == CommandTypes.C_PUSH or \
                    parser.commandType() == CommandTypes.C_POP) and \
                    arg1 is not None and arg2 is not None:
                code_writer.writePushPop(parser.commandType(), arg1, arg2)
            
            if parser.commandType() == CommandTypes.C_LABEL and arg1 is not None:
                code_writer.writeLabel(arg1)
            
            if parser.commandType() == CommandTypes.C_GOTO and arg1 is not None:
                code_writer.writeGoto(arg1)
            
            if parser.commandType() == CommandTypes.C_IF and arg1 is not None:
                code_writer.writeIf(arg1)

            if parser.commandType() == CommandTypes.C_FUNCTION and \
                    arg1 is not None and arg2 is not None:
                code_writer.writeFunction(arg1, arg2)
            
            if parser.commandType() == CommandTypes.C_CALL and \
                    arg1 is not None and arg2 is not None:
                code_writer.writeCall(arg1, arg2)
            
            if parser.commandType() == CommandTypes.C_RETURN:
                code_writer.writeReturn()
        
    code_writer.close()

if __name__ == "__main__":
    main()
