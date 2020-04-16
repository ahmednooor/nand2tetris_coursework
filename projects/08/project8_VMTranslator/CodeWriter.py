import os
import sys
import uuid

from Utils import *

class CodeWriter:
    ASM_CODE_TEMPLATES_PATH = os.getcwd() + "/asm_code_templates/"

    C_UNKNOWN = CommandTypes.C_UNKNOWN
    C_ARITHMETIC = CommandTypes.C_ARITHMETIC
    C_PUSH = CommandTypes.C_PUSH
    C_POP = CommandTypes.C_POP
    C_LABEL = CommandTypes.C_LABEL
    C_GOTO = CommandTypes.C_GOTO
    C_IF = CommandTypes.C_IF
    C_FUNCTION = CommandTypes.C_FUNCTION
    C_RETURN = CommandTypes.C_RETURN
    C_CALL = CommandTypes.C_CALL
    
    ARITHMETIC_SYMBOLS = {
        "add": "+",
        "sub": "-",
        "neg": "-",
        "eq": "JEQ",
        "gt": "JGT",
        "lt": "JLT",
        "and": "&",
        "or": "|",
        "not": "!",
    }

    SEGMENT_NAMES = {
        "argument": "ARG",
        "local": "LCL",
        "static": "static",
        "constant": "constant",
        "this": "THIS",
        "that": "THAT",
        "pointer": "THIS",
        "temp": "R5",
    }

    def __init__(self, output_file_url):
        self.output_file_url = output_file_url.split(".")
        
        if len(self.output_file_url) > 1:
            self.output_file_url.pop()
        
        self.output_file_url.append("asm")
        
        self.output_file_url = ".".join(self.output_file_url)
        self.output_file = open(self.output_file_url, "w")

        code_to_write = ""
        
        with open(self.ASM_CODE_TEMPLATES_PATH + "header_boilerplate.asm", "r") as f:
            code_to_write = f.read()

        self.output_file.write(code_to_write)

        self.current_function = "Sys.init"
        self.funcs_call_counts = {}
        
    def setFileName(self, input_file_name):
        self.input_file_name = os.path.basename(input_file_name)
        self.output_file.write("// [File] " + self.input_file_name + "\n")
        self.input_file_name = self.input_file_name.split(".")
        
        if len(self.input_file_name) > 1:
            self.input_file_name.pop()

        self.input_file_name = ".".join(self.input_file_name)
        self.SEGMENT_NAMES["static"] = self.input_file_name

    def writeInit(self):
        code_to_write = ""
        
        with open(self.ASM_CODE_TEMPLATES_PATH + "init.asm", "r") as f:
            code_to_write = f.read()

        self.output_file.write(code_to_write)

    def writeArithmetic(self, command):
        if command not in self.ARITHMETIC_SYMBOLS:
            raise Exception("Error[5]: Invalid arithmetic command \"" + command + "\"")
        
        code_to_write = ""
        
        if command == "add" or command == "sub" or command == "and" or command == "or":
            code_to_write = self._getAddSubAndOrCode(command)
        elif command == "neg" or command == "not":
            code_to_write = self._getNegNotCode(command)
        elif command == "eq" or command == "gt" or command == "lt":
            code_to_write = self._getEqGtLtCode(command)

        self.output_file.write(code_to_write)

    def writePushPop(self, command_type, segment, index):
        if command_type != self.C_PUSH and command_type != self.C_POP:
            raise Exception("Error[6]: Invalid push/pop command \"" + command_type + "\"")
        
        if segment not in self.SEGMENT_NAMES:
            raise Exception("Error[7]: Invalid segment name \"" + segment + "\"")
            
        code_to_write = ""

        if command_type == self.C_PUSH:
            code_to_write = self._getPushCode("push", segment, index)
        
        if command_type == self.C_POP:
            code_to_write = self._getPopCode("pop", segment, index)

        self.output_file.write(code_to_write)

    def writeLabel(self, label):
        code_to_write = ""
        label = self.current_function + "$" + label

        with open(self.ASM_CODE_TEMPLATES_PATH + "label.asm", "r") as f:
            code_to_write = f.read()
            code_to_write = code_to_write.replace("_{%LABEL%}_", label)
        
        self.output_file.write(code_to_write)

    def writeGoto(self, label):
        code_to_write = ""
        label = self.current_function + "$" + label

        with open(self.ASM_CODE_TEMPLATES_PATH + "goto.asm", "r") as f:
            code_to_write = f.read()
            code_to_write = code_to_write.replace("_{%LABEL%}_", label)
        
        self.output_file.write(code_to_write)
    
    def writeIf(self, label):
        code_to_write = ""
        label = self.current_function + "$" + label

        with open(self.ASM_CODE_TEMPLATES_PATH + "if_goto.asm", "r") as f:
            code_to_write = f.read()
            code_to_write = code_to_write.replace("_{%LABEL%}_", label)
        
        self.output_file.write(code_to_write)
        
    def writeCall(self, function_name, n_args):
        if function_name not in self.funcs_call_counts:
            self.funcs_call_counts[function_name] = 0
        
        self.funcs_call_counts[function_name] += 1

        code_to_write = ""

        with open(self.ASM_CODE_TEMPLATES_PATH + "call.asm", "r") as f:
            code_to_write = f.read()
            code_to_write = code_to_write.replace("_{%FUNCNAME%}_", function_name)
            code_to_write = code_to_write.replace("_{%CALLCOUNT%}_", str(self.funcs_call_counts[function_name]))
            code_to_write = code_to_write.replace("_{%NARGS%}_", n_args)
        
        self.output_file.write(code_to_write)
        
    def writeFunction(self, function_name, n_vars):
        self.current_function = function_name
        code_to_write = ""

        with open(self.ASM_CODE_TEMPLATES_PATH + "function.asm", "r") as f:
            code_to_write = f.read()
            code_to_write = code_to_write.replace("_{%FUNCNAME%}_", function_name)
            code_to_write = code_to_write.replace("_{%NVARS%}_", n_vars)
        
        self.output_file.write(code_to_write)
    
    def writeReturn(self):
        code_to_write = ""

        with open(self.ASM_CODE_TEMPLATES_PATH + "return.asm", "r") as f:
            code_to_write = f.read()
        
        self.output_file.write(code_to_write)

    def close(self):
        code_to_write = ""
        
        with open(self.ASM_CODE_TEMPLATES_PATH + "footer_boilerplate.asm", "r") as f:
            code_to_write = f.read()

        self.output_file.write(code_to_write)
        self.output_file.close()

    def _getPushCode(self, command, segment, index):
        code_to_write = ""

        if segment == "constant":
            with open(self.ASM_CODE_TEMPLATES_PATH + "push_constant.asm", "r") as f:
                code_to_write = f.read()
                code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
                code_to_write = code_to_write.replace("_{%INDEX%}_", index)

        if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            with open(self.ASM_CODE_TEMPLATES_PATH + "push_lcl_arg_this_that.asm", "r") as f:
                code_to_write = f.read()
                code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
                code_to_write = code_to_write.replace("_{%SEGMENT%}_", self.SEGMENT_NAMES[segment])
                code_to_write = code_to_write.replace("_{%INDEX%}_", index)

        if segment == "temp" or segment == "pointer":
            with open(self.ASM_CODE_TEMPLATES_PATH + "push_temp_pointer.asm", "r") as f:
                code_to_write = f.read()
                code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
                code_to_write = code_to_write.replace("_{%SEGMENT%}_", self.SEGMENT_NAMES[segment])
                code_to_write = code_to_write.replace("_{%INDEX%}_", index)
        
        if segment == "static":
            with open(self.ASM_CODE_TEMPLATES_PATH + "push_static.asm", "r") as f:
                code_to_write = f.read()
                code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
                code_to_write = code_to_write.replace("_{%FILE%}_", self.SEGMENT_NAMES[segment])
                code_to_write = code_to_write.replace("_{%INDEX%}_", index)
            
        return code_to_write

    def _getPopCode(self, command, segment, index):
        code_to_write = ""

        if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            with open(self.ASM_CODE_TEMPLATES_PATH + "pop_lcl_arg_this_that.asm", "r") as f:
                code_to_write = f.read()
                code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
                code_to_write = code_to_write.replace("_{%SEGMENT%}_", self.SEGMENT_NAMES[segment])
                code_to_write = code_to_write.replace("_{%INDEX%}_", index)

        if segment == "temp" or segment == "pointer":
            with open(self.ASM_CODE_TEMPLATES_PATH + "pop_temp_pointer.asm", "r") as f:
                code_to_write = f.read()
                code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
                code_to_write = code_to_write.replace("_{%SEGMENT%}_", self.SEGMENT_NAMES[segment])
                code_to_write = code_to_write.replace("_{%INDEX%}_", index)
        
        if segment == "static":
            with open(self.ASM_CODE_TEMPLATES_PATH + "pop_static.asm", "r") as f:
                code_to_write = f.read()
                code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
                code_to_write = code_to_write.replace("_{%FILE%}_", self.SEGMENT_NAMES[segment])
                code_to_write = code_to_write.replace("_{%INDEX%}_", index)
            
        return code_to_write

    def _getAddSubAndOrCode(self, command):
        code_to_write = ""

        with open(self.ASM_CODE_TEMPLATES_PATH + "add_sub_and_or.asm", "r") as f:
            code_to_write = f.read()
            code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
            code_to_write = code_to_write.replace("_{%SYMBOL%}_", self.ARITHMETIC_SYMBOLS[command])
        
        return code_to_write

    def _getNegNotCode(self, command):
        code_to_write = ""

        with open(self.ASM_CODE_TEMPLATES_PATH + "neg_not.asm", "r") as f:
            code_to_write = f.read()
            code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
            code_to_write = code_to_write.replace("_{%SYMBOL%}_", self.ARITHMETIC_SYMBOLS[command])

        return code_to_write

    def _getEqGtLtCode(self, command):
        code_to_write = ""
        uuid_str = str(uuid.uuid4()).replace("-", "")

        with open(self.ASM_CODE_TEMPLATES_PATH + "eq_gt_lt.asm", "r") as f:
            code_to_write = f.read()
            code_to_write = code_to_write.replace("_{%COMMAND%}_", command)
            code_to_write = code_to_write.replace("_{%SYMBOL%}_", self.ARITHMETIC_SYMBOLS[command])
            code_to_write = code_to_write.replace("_{%UUID%}_", uuid_str)

        return code_to_write
