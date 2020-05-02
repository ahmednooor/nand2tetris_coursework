import os

class Parser:

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
            
            # ommit white spaces
            self.source_lines[i] = "".join([x for x in self.source_lines[i].split(" ") if x != ""])

        self.tokens = []
        self.total_lines = len(self.source_lines)
        self.current_instruction = -1
        self.symbol_table = {
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
        }

        # [print(x) for x in self.source_lines]
        # [print(x) for x in self.tokens]
        # print(self.total_lines)
        self.parse_instructions()

    def parse_instructions(self):
        for index, line in enumerate(self.source_lines):
            if line is None:
                continue

            if line[0] == "@":
                self.parse_a_instruction(line, index)
            elif line[0] == "(":
                self.parse_label(line, index)
            else:
                self.parse_c_instruction(line, index)

    def parse_a_instruction(self, line, index):
        self.current_instruction += 1

        token = self._get_token_template()
        token["obj_line_num"] = self.current_instruction
        token["src_line_num"] = index + 1
        token["instruction_type"] = "A"
        token["value"] = line[1::]
        token["dest"] = None
        token["comp"] = None
        token["jump"] = None
        
        self.tokens.append(token)
        # print(token)

    def parse_c_instruction(self, line, index):
        self.current_instruction += 1

        token = self._get_token_template()
        token["obj_line_num"] = self.current_instruction
        token["src_line_num"] = index + 1
        token["instruction_type"] = "C"
        token["value"] = None
        token["dest"] = None
        token["comp"] = None
        token["jump"] = None
        
        line_len = len(line)
        breakpoint_index = 0
        for i in range(0, line_len):
            if line[i] == "=":
                breakpoint_index = i + 1
                token["dest"] = line[0:i]
            elif i == line_len-1:
                token["comp"] = line[breakpoint_index::]
            elif line[i] == ";":
                token["comp"] = line[breakpoint_index:i]
                token["jump"] = line[i+1::]
                break
        
        self.tokens.append(token)

    def parse_label(self, line, index):
        if line[-1] != ")":
            raise Exception("Line:" + str(index+1) + " ERR: ')' expected at end.")
        
        if line[1] in "-":
            raise Exception("Line:" + str(index+1) + " ERR: Labels can't start with a number or '-' sign.")
        
        label = line[1:-1]
        if label in self.symbol_table:
            return

        self.symbol_table[label] = self.current_instruction + 1

    def _get_token_template(self):
        return {
            "obj_line_num": 0,
            "src_line_num": 0,
            "instruction_type": "",
            "value": "",
            "dest": "",
            "comp": "",
            "jump": ""
        }
