import os
import sys

from Utils import *

class Parser:
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

    COMMAND_TYPES = {
        "add": CommandTypes.C_ARITHMETIC,
        "sub": CommandTypes.C_ARITHMETIC,
        "neg": CommandTypes.C_ARITHMETIC,
        "eq": CommandTypes.C_ARITHMETIC,
        "gt": CommandTypes.C_ARITHMETIC,
        "lt": CommandTypes.C_ARITHMETIC,
        "and": CommandTypes.C_ARITHMETIC,
        "or": CommandTypes.C_ARITHMETIC,
        "not": CommandTypes.C_ARITHMETIC,
        "push": CommandTypes.C_PUSH,
        "pop": CommandTypes.C_POP,
        "label": CommandTypes.C_LABEL,
        "goto": CommandTypes.C_GOTO,
        "if-goto": CommandTypes.C_IF,
        "call": CommandTypes.C_CALL,
        "function": CommandTypes.C_FUNCTION,
        "return": CommandTypes.C_RETURN,
    }

    def __init__(self, input_file_url):
        if not os.path.isfile(input_file_url):
            raise FileNotFoundError("Error[1]: File \"" + input_file_url + "\" Not Found")

        with open(input_file_url, "r") as f:
            self.source_lines = f.read().split("\n")

        for i in range(0, len(self.source_lines)):
            if len(self.source_lines[i]) == 0:
                self.source_lines[i] = None
                continue
            
            if len(self.source_lines[i]) > 1 and self.source_lines[i][0:2] == "//":
                self.source_lines[i] = None
                continue

            if self.source_lines[i].find("//") != -1:
                self.source_lines[i] = self.source_lines[i][0:self.source_lines[i].find("//")]
            
            # ommit extra white spaces
            self.source_lines[i] = " ".join([x for x in self.source_lines[i].split(" ") if x != ""])

        self.total_lines = len(self.source_lines)
        self.current_line_index = -1

        if self.total_lines == 0:
            self.current_line_index = 0

        self.current_command = {
            "line_num": 0,
            "tokens": [],
            "command_type": 0,
            "arg1": "",
            "arg2": 0,
        }

    def hasMoreCommands(self):
        self.current_line_index += 1

        if self.current_line_index > self.total_lines-1:
            self.current_line_index -= 1
            return False
        
        if self.source_lines[self.current_line_index] is None:
            return self.hasMoreCommands()
        
        self.current_line_index -= 1
        return True

    def advance(self):
        if not self.hasMoreCommands():
            raise Exception("Error[4]: No more commands left to advance(). " + \
                            "Check hasMoreCommands() output before calling advance()")
        
        self.current_line_index += 1
        self.current_command["line_num"] = self.current_line_index + 1
        self.current_command["tokens"] = self.source_lines[self.current_line_index].split(" ")
        self.current_command["command_type"] = self._getCommandType()
        self.current_command["arg2"] = 0

        if self.current_command["command_type"] == self.C_ARITHMETIC:
            self.current_command["arg1"] = self.current_command["tokens"][0]
        else:
            self.current_command["arg1"] = ""
        
        if self.current_command["command_type"] == self.C_PUSH or \
                self.current_command["command_type"] == self.C_POP or \
                self.current_command["command_type"] == self.C_FUNCTION or \
                self.current_command["command_type"] == self.C_CALL:
            self.current_command["arg1"] = self.current_command["tokens"][1]
            self.current_command["arg2"] = self.current_command["tokens"][2]
        
        if self.current_command["command_type"] == self.C_LABEL or \
                self.current_command["command_type"] == self.C_GOTO or \
                self.current_command["command_type"] == self.C_IF:
            self.current_command["arg1"] = self.current_command["tokens"][1]
        
        print(self.current_command)

    def commandType(self):
        return self.current_command["command_type"]
    
    def arg1(self):
        if self.commandType() == self.C_RETURN:
            raise Exception("Error[2]: arg1() should not be called, if the command type is C_RETURN. " + \
                            "Check commandType() output before calling arg1()")
    
        return self.current_command["arg1"]
    
    def arg2(self):
        if self.commandType() != self.C_PUSH and \
                self.commandType() != self.C_POP and \
                self.commandType() != self.C_FUNCTION and \
                self.commandType() != self.C_CALL:
            raise Exception("Error[3]: arg2() should only be called, if the command type is one of " + \
                            "(C_PUSH, C_POP, C_FUNCTION, C_CALL). Check commandType() output before calling arg2()")
        
        return self.current_command["arg2"]

    def _getCommandType(self):
        command = self.current_command["tokens"][0]

        if command in self.COMMAND_TYPES:
            return self.COMMAND_TYPES[command]
        
        return self.C_UNKNOWN
