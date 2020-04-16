import os
import sys
import re

from utils import *

class JackTokenizer:

    TOKEN_TYPES = {
        "keyword": TokenType.KEYWORD,
        "identifier": TokenType.IDENTIFIER,
        "integerConstant": TokenType.INT_CONST,
        "stringConstant": TokenType.STRING_CONST,
        "symbol": TokenType.SYMBOL,
    }

    KEYWORDS = {
        "class": KeyWord.CLASS,
        "constructor": KeyWord.CONSTRUCTOR,
        "function": KeyWord.FUNCTION,
        "method": KeyWord.METHOD,
        "field": KeyWord.FIELD,
        "static": KeyWord.STATIC,
        "var": KeyWord.VAR,
        "int": KeyWord.INT,
        "char": KeyWord.CHAR,
        "boolean": KeyWord.BOOLEAN,
        "void": KeyWord.VOID,
        "true": KeyWord.TRUE,
        "false": KeyWord.FALSE,
        "null": KeyWord.NULL,
        "this": KeyWord.THIS,
        "let": KeyWord.LET,
        "do": KeyWord.DO,
        "if": KeyWord.IF,
        "else": KeyWord.ELSE,
        "while": KeyWord.WHILE,
        "return": KeyWord.RETURN,
    }

    SYMBOLS = {
        "{": "{",
        "}": "}",
        "(": "(",
        ")": ")",
        "[": "[",
        "]": "]",
        ".": ".",
        ",": ",",
        ";": ";",
        "+": "+",
        "-": "-",
        "*": "*",
        "/": "/",
        "&": "&",
        "|": "|",
        "<": "<",
        ">": ">",
        "=": "=",
        "~": "~",
    }

    def __init__(self, input_file_url):
        if not os.path.isfile(input_file_url):
            raise FileNotFoundError("Error[1]: File \"" + input_file_url + "\" not found.")

        self.chars = ""
        self.chars_lines = []
        self.current_line = 1
        self.tokens = [] # [(line_num:int, column_num:int, token_type:str, token_val:str)]
        self.cur_index = 0
        self.chars_len = 0

        with open(input_file_url, "r") as f:
            self.chars = f.read()
            self.chars_len = len(self.chars)

        self._tokenize()

        # for x in self.tokens:
        #     print(x)
        
        self.cur_token_index = -1
        self.tokens_len = len(self.tokens)
        self.current_token = ()

        self.output_file_url = input_file_url.split(".")
        
        if self.output_file_url[-1] == "jack":
            self.output_file_url.pop()
        
        self.output_file_url[-1] = self.output_file_url[-1] + "T"
        self.output_file_url.append("xml")
        self.output_file_url = ".".join(self.output_file_url)
        
        # self.writeOutputXmlFile()

    def writeOutputXmlFile(self):
        xml_safe_chars = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
        }
        output_file = open(self.output_file_url, "w")
        output_file.write("<tokens>\n")

        for token in self.tokens:
            token_val = token[3]
            
            if token_val in xml_safe_chars:
                token_val = xml_safe_chars[token_val]

            output_file.write("<" + token[2] + "> ")
            output_file.write(token_val)
            output_file.write(" </" + token[2] + ">\n")
        
        output_file.write("</tokens>\n")
        output_file.close()
        
    def hasMoreTokens(self):
        if self.cur_token_index+1 < self.tokens_len:
            return True
        
        return False

    def advance(self):
        if not self.hasMoreTokens():
            raise Exception("Error[2] No more tokens left to advance.")

        self.cur_token_index += 1
        self.current_token = self.tokens[self.cur_token_index]

    def tokenType(self):
        if self.current_token[2] not in self.TOKEN_TYPES:
            raise Exception("Error[3] Unrecognized token '" + self.current_token[2] + "'.")
        
        return self.TOKEN_TYPES[self.current_token[2]]
    
    def keyword(self):
        if self.tokenType() != TokenType.KEYWORD:
            raise Exception("Error[4] keyword() should only be called when tokenType() is a KEYWORD.")
        
        if self.current_token[3] not in self.KEYWORDS:
            raise Exception("Error[5] Unrecognized keyword '" + self.current_token[3] + "'.")
        
        return self.KEYWORDS[self.current_token[3]]
    
    def symbol(self):
        if self.tokenType() != TokenType.SYMBOL:
            raise Exception("Error[6] symbol() should only be called when tokenType() is a SYMBOL.")
        
        if self.current_token[3] not in self.SYMBOLS:
            raise Exception("Error[7] Unrecognized symbol '" + self.current_token[3] + "'.")
        
        return self.SYMBOLS[self.current_token[3]]
    
    def identifier(self):
        if self.tokenType() != TokenType.IDENTIFIER:
            raise Exception("Error[8] identifier() should only be called when tokenType() is a IDENTIFIER.")
        
        return self.SYMBOLS[self.current_token[3]]
    
    def intVal(self):
        if self.tokenType() != TokenType.INT_CONST:
            raise Exception("Error[9] intVal() should only be called when tokenType() is a INT_CONST.")
        
        return int(self.SYMBOLS[self.current_token[3]])
    
    def stringVal(self):
        if self.tokenType() != TokenType.STRING_CONST:
            raise Exception("Error[10] stringVal() should only be called when tokenType() is a STRING_CONST.")
        
        return self.SYMBOLS[self.current_token[3]]

    def _tokenize(self):
        while self.cur_index < self.chars_len:
            c = self.chars[self.cur_index]
            
            if c == "/" and self.cur_index < (self.chars_len-1) and self.chars[self.cur_index+1] == "/":
                self._scan_single_line_comment()
            elif c == "/" and self.cur_index < (self.chars_len-1) and self.chars[self.cur_index+1] == "*":
                self._scan_multi_line_comment()
            elif c == "\"":
                self._scan_string_constant()
            elif re.match("[0-9]", c):
                self._scan_integer_constant()
            elif c in self.SYMBOLS:
                self._scan_symbol()
            elif re.match("[_a-zA-Z]", c):
                self._scan_identifier_and_keyword()
            elif c == "\n" or c == "\r\n":
                self.current_line += 1
            elif c not in " \n\t":
                raise Exception(self._get_cur_line_col() + \
                                " Unexpected character '" + self.chars[self.cur_index] + "' found")

            self.cur_index += 1

    def _scan_string_constant(self):
        token_chars = []
        self.cur_index += 1
        
        while self.cur_index < self.chars_len:
            c = self.chars[self.cur_index]
        
            if c == "\"" and self.chars[self.cur_index-1] != "\\":
                break
            if c == "\n":
                raise Exception(self._get_cur_line_col(len(token_chars)) + " Expected '\"' but found '\\n'")
            
            token_chars.append(c)
            self.cur_index += 1
        
        self.tokens.append((
            self._get_cur_line(), 
            self._get_cur_column()-len(token_chars), 
            "stringConstant", 
            "".join(token_chars)))
    
    def _scan_integer_constant(self):
        token_chars = []
        
        while self.cur_index < self.chars_len:
            c = self.chars[self.cur_index]

            if c == "\n" or c == "\r\n":
                self.current_line += 1

            if c == " " or c == "\n" or c in self.SYMBOLS:
                break
            
            if re.match("[_a-zA-Z]", c) or not re.match("[0-9]", c):
                raise Exception(self._get_cur_line_col(len(token_chars)) + \
                                " Unexpected character '" + self.chars[self.cur_index] + "' found in integer")
            
            token_chars.append(c)
            self.cur_index += 1
        
        if int("".join(token_chars)) > 32767:
            raise Exception(self._get_cur_line_col(len(token_chars)) + " Integer can only be 0 to 32767")
        
        self.tokens.append((
            self._get_cur_line(), 
            self._get_cur_column()-len(token_chars), 
            "integerConstant", 
            "".join(token_chars)))
        self.cur_index -= 1
    
    def _scan_symbol(self):
        self.tokens.append((
            self._get_cur_line(), 
            self._get_cur_column(), 
            "symbol", 
            self.SYMBOLS[self.chars[self.cur_index]]))
    
    def _scan_identifier_and_keyword(self):
        token_chars = []
        
        while self.cur_index < self.chars_len:
            c = self.chars[self.cur_index]
        
            if c == "\n" or c == "\r\n":
                self.current_line += 1

            if c == " " or c == "\n" or c in self.SYMBOLS:
                break
            
            if not re.match("[_a-zA-Z]", c) and not re.match("[0-9]", c):
                raise Exception(self._get_cur_line_col(len(token_chars)) + \
                                " Unexpected character '" + self.chars[self.cur_index] + "' found in identifier")
            
            token_chars.append(c)
            self.cur_index += 1
        
        token_chars = "".join(token_chars)

        if token_chars in self.KEYWORDS:
            self.tokens.append((
                self._get_cur_line(), 
                self._get_cur_column()-len(token_chars), 
                "keyword", 
                token_chars))
        else:
            self.tokens.append((
                self._get_cur_line(), 
                self._get_cur_column()-len(token_chars), 
                "identifier", 
                token_chars))
        
        self.cur_index -= 1
    
    def _scan_single_line_comment(self):
        self.cur_index += 2
        
        while self.cur_index < self.chars_len:
            c = self.chars[self.cur_index]
        
            if c == "\n" or c == "\r\n":
                self.current_line += 1
                break
            
            self.cur_index += 1
        
    def _scan_multi_line_comment(self):
        self.cur_index += 2
        
        while self.cur_index < self.chars_len:
            c = self.chars[self.cur_index]
        
            if c == "*" and self.cur_index < (self.chars_len-1) and self.chars[self.cur_index+1] == "/":
                self.cur_index += 1
                break

            if c == "\n" or c == "\r\n":
                self.current_line += 1
            
            self.cur_index += 1

    def _get_cur_line_col(self, col_offset=0):
        ln = str(self._get_cur_line())
        col = str(self._get_cur_column()-col_offset)
        return "[L:" + ln + ",C:" + col + "]"

    def _get_cur_line(self):
        return self.current_line
    
    def _get_cur_column(self):
        return self.cur_index - len("\n".join(self.chars.split("\n")[0:self.current_line-1]))
