import os
import re


class CodeWriter:

    comp_map = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101",
    }

    dest_map = {
        "null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111",
    }

    jump_map = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    def __init__(self, input_file_url, tokens, symbol_table):
        self.output_file_url = input_file_url.split(".")
        
        if self.output_file_url[-1] == "asm":
            self.output_file_url.pop()
        
        self.output_file_url.append("hack")
        self.output_file_url = ".".join(self.output_file_url)

        self.tokens = tokens
        self.symbol_table = symbol_table
        self.binary_instructions = []
        self.variable_count = 15

        self.process_tokens()
        self.write_output_file()

    def process_tokens(self):
        for index, token in enumerate(self.tokens):
            if token["instruction_type"] == "A":
                self.write_a_instruction(token, index)
            elif token["instruction_type"] == "C":
                self.write_c_instruction(token, index)

    def write_a_instruction(self, token, index):
        if re.match("[0-9]", token["value"]) and int(token["value"]) > 32767:
            raise Exception("Line:" + str(token["src_line_num"]) + " ERR: Numeric values can only be between 0 to 32767.")
        
        if token["value"][0] in "-":
            raise Exception("Line:" + str(token["src_line_num"]) + " ERR: Variables can't start with a number or '-' sign.")

        bin_instruction_value = 0

        if re.match("[0-9]", token["value"]) and int(token["value"]) < 32768:
            bin_instruction_value = int(token["value"])
        elif token["value"] in self.symbol_table:
            bin_instruction_value = self.symbol_table[token["value"]]
        else:
            self.variable_count += 1
            bin_instruction_value = self.variable_count
            self.symbol_table[token["value"]] = bin_instruction_value

        self.binary_instructions.append("0" + "{0:015b}".format(bin_instruction_value))
    
    def write_c_instruction(self, token, index):
        if token["comp"] is None or token["comp"] == "":
            raise Exception("Line:" + str(token["src_line_num"]) + " ERR: Expected 'comp' part of C instruction not found.")
        
        if token["dest"] == "":
            raise Exception("Line:" + str(token["src_line_num"]) + " ERR: Expected 'dest' part of C instruction not found.")
        
        if token["jump"] == "":
            raise Exception("Line:" + str(token["src_line_num"]) + " ERR: Expected 'jump' part of C instruction not found.")

        if token["dest"] is None:
            token["dest"] = "null"
        
        if token["jump"] is None:
            token["jump"] = "null"

        if token["comp"] not in self.comp_map:
            raise Exception("Line:" + str(token["src_line_num"]) \
                            + " ERR: Invalid comp part '" + token["comp"] + "' in C instruction.")
        
        if token["dest"] not in self.dest_map:
            raise Exception("Line:" + str(token["src_line_num"]) \
                            + " ERR: Invalid dest part '" + token["dest"] + "' in C instruction.")
        
        if token["jump"] not in self.jump_map:
            raise Exception("Line:" + str(token["src_line_num"]) \
                            + " ERR: Invalid jump part '" + token["jump"] + "' in C instruction.")

        bin_instruction_value = "111" \
                                + self.comp_map[token["comp"]] \
                                + self.dest_map[token["dest"]] \
                                + self.jump_map[token["jump"]]
        
        self.binary_instructions.append(bin_instruction_value)

    def write_output_file(self):
        with open(self.output_file_url, "w") as f:
            f.write("\n".join(self.binary_instructions) + "\n")
