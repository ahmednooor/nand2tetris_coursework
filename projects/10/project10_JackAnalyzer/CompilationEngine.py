# ##############################################################################
# //////////////////////////////////////////////////////////////////////////////
# 
# READ THIS FIRST BEFORE LOOKING AT THE CODE
# 
# REGARDING CODE QUALITY, JUST DON'T ASK. COMPILERS ARE F**KING HARD. 
# AND NOW I FEEL LIKE A DUMB STUPID PIECE OF SH*T. 
# I STILL F**KING CAN'T BELIEVE THAT IT ACTUALLY WORKED. 
# IF CODING HAD A FORM OF METASTASIZED CANCER, THIS WOULD BE IT. 
# I AM IN COMPLETE AWE OF THE MINDS WHO ACTUALLY THOUGHT OF STUFF LIKE 
# LANGUAGES, GRAMMARS, FIRST, FOLLOW, PARSERS AND PARSING TECHNIQUES ETC. 
# AND THE ONES WHO IMPLEMENTED THAT STUFF RIGHT.
# P.S. I DIDN'T/COULDN'T FOLLOW ANY OF THOSE TECHNIQUES AND WENT STRAIGHT INTO 
# THE RABBIT HOLE, HENCE THIS MESS.
# 
# I REALLY WANT TO CODE IT BETTER, BUT I DON'T HAVE ANY ENERGY OR WILL LEFT.
# 
# //////////////////////////////////////////////////////////////////////////////
# ##############################################################################

import os
import sys
import json
import pprint

from utils import *

class CompilationEngine:

    def __init__(self, tokens, input_file_url):

        self.tokens = tokens
        self.tokens_len = len(tokens)
        self.cur_token_index = 0
        self.current_token = ()
        self.parse_tree = {
            "node_name": "root",
            "children": [],
            "parent": None,
        }
        self.current_node = self.parse_tree

        self.output_file_url = input_file_url.split(".")
        
        if self.output_file_url[-1] == "jack":
            self.output_file_url.pop()
        
        self.output_file_url.append("xml")
        self.output_file_url = ".".join(self.output_file_url)
        self.output_file = open(self.output_file_url, "w")

        self.startCompilation()
        # pprint.pprint(self.parse_tree)
        
        self.writeOutputXmlFile(self.parse_tree["children"][-1])
        self.output_file.close()

    def startCompilation(self):
        while self.cur_token_index < self.tokens_len:
            self.current_token = self.tokens[self.cur_token_index]
            self.compileClass()
            self.cur_token_index += 1

    def _advance_token(self):
        self.cur_token_index += 1
        self.current_token = self.tokens[self.cur_token_index]

    def _reverse_token(self):
        self.cur_token_index -= 1
        self.current_token = self.tokens[self.cur_token_index]

    def compileClass(self):
        if self.current_token[2] != "keyword" or \
                self.current_token[3] != "class":
            pprint.pprint(self.parse_tree)
            raise Exception("1 " + str(self.current_token))
        self.current_node["children"].append({
            "node_name": "class",
            "children": [],
            "parent": self.parse_tree,
        })
        self.current_node = self.current_node["children"][-1]
        self._addTokenLeafNode()
        
        self._advance_token()
        if self.current_token[2] != "identifier":
            pprint.pprint(self.parse_tree)
            raise Exception("2 " + str(self.current_token))
        self._addTokenLeafNode()

        self._advance_token()
        if self.current_token[2] != "symbol" or self.current_token[3] != "{":
            pprint.pprint(self.parse_tree)
            raise Exception("3 " + str(self.current_token))
        self._addTokenLeafNode()

        self.compileClassVarDec()
        self.compileSubroutine()

        self._advance_token()
        if self.current_token[2] != "symbol" or self.current_token[3] != "}":
            pprint.pprint(self.parse_tree)
            raise Exception("3 " + str(self.current_token))
        self._addTokenLeafNode()

    def compileClassVarDec(self):
        while True:
            self._advance_token()
            if self.current_token[2] != "keyword":
                self._reverse_token()
                return
            if self.current_token[2] == "keyword" and \
                    self.current_token[3] != "static" and \
                    self.current_token[3] != "field":
                self._reverse_token()
                return
            self.current_node["children"].append({
                "node_name": "classVarDec",
                "children": [],
                "parent": self.current_node,
            })
            self.current_node = self.current_node["children"][-1]
            self._addTokenLeafNode()

            self._advance_token()
            if self.current_token[2] != "keyword" and \
                    self.current_token[2] != "identifier":
                pprint.pprint(self.parse_tree)
                raise Exception("3 " + str(self.current_token))
            if self.current_token[2] == "keyword" and \
                    self.current_token[3] not in ["int", "char", "boolean"]:
                pprint.pprint(self.parse_tree)
                raise Exception("4 " + str(self.current_token))
            self._addTokenLeafNode()

            self._advance_token()
            if self.current_token[2] != "identifier":
                pprint.pprint(self.parse_tree)
                raise Exception("5 " + str(self.current_token))
            self._addTokenLeafNode()

            self._advance_token()
            while self.current_token[2] == "symbol" and self.current_token[3] == "," and \
                    self.tokens[self.cur_token_index+1][2] == "identifier":
                self._addTokenLeafNode()
                self._advance_token()
                self._addTokenLeafNode()
                self._advance_token()
            
            if self.current_token[2] != "symbol" or self.current_token[3] != ";":
                pprint.pprint(self.parse_tree)
                raise Exception("5 " + str(self.current_token))
            self._addTokenLeafNode()

            self.current_node = self.current_node["parent"]

    def compileSubroutine(self):
        while True:
            self._advance_token()
            if self.current_token[2] != "keyword":
                self._reverse_token()
                return
            if self.current_token[2] == "keyword" and \
                    self.current_token[3] != "constructor" and \
                    self.current_token[3] != "method" and \
                    self.current_token[3] != "function":
                self._reverse_token()
                return
            self.current_node["children"].append({
                "node_name": "subroutineDec",
                "children": [],
                "parent": self.current_node,
            })
            self.current_node = self.current_node["children"][-1]
            self._addTokenLeafNode()

            self._advance_token()
            if self.current_token[2] != "keyword" and \
                    self.current_token[2] != "identifier":
                pprint.pprint(self.parse_tree)
                raise Exception("6 " + str(self.current_token))
            if self.current_token[2] == "keyword" and \
                    self.current_token[3] not in ["void", "int", "char", "boolean"]:
                pprint.pprint(self.parse_tree)
                raise Exception("7 " + str(self.current_token))
            self._addTokenLeafNode()

            self._advance_token()
            if self.current_token[2] != "identifier":
                pprint.pprint(self.parse_tree)
                raise Exception("8 " + str(self.current_token))
            self._addTokenLeafNode()
            
            self._advance_token()
            if self.current_token[2] != "symbol" or self.current_token[3] != "(":
                pprint.pprint(self.parse_tree)
                raise Exception("9 " + str(self.current_token))
            self._addTokenLeafNode()

            self.compileParameterList()

            self._advance_token()
            if self.current_token[2] != "symbol" or self.current_token[3] != ")":
                pprint.pprint(self.parse_tree)
                raise Exception("10 " + str(self.current_token))
            self._addTokenLeafNode()
            
            self.current_node["children"].append({
                "node_name": "subroutineBody",
                "children": [],
                "parent": self.current_node,
            })
            self.current_node = self.current_node["children"][-1]
            
            self._advance_token()
            if self.current_token[2] != "symbol" or self.current_token[3] != "{":
                pprint.pprint(self.parse_tree)
                raise Exception("10 " + str(self.current_token))
            self._addTokenLeafNode()

            self.compileVarDec()
            self._reverse_token()
            self.compileStatements()

            # self._advance_token()
            if self.current_token[2] != "symbol" or self.current_token[3] != "}":
                pprint.pprint(self.parse_tree)
                raise Exception("10 " + str(self.current_token))
            self._addTokenLeafNode()
            self.current_node = self.current_node["parent"]
            self.current_node = self.current_node["parent"]

    def compileParameterList(self):
        self.current_node["children"].append({
            "node_name": "parameterList",
            "children": [],
            "parent": self.current_node,
        })

        self._advance_token()
        if self.current_token[2] != "keyword" and \
                self.current_token[2] != "identifier":
            self._reverse_token()
            return
        if self.current_token[2] == "keyword" and \
                self.current_token[3] not in ["int", "char", "boolean"]:
            self._reverse_token()
            return
        self.current_node = self.current_node["children"][-1]
        self._addTokenLeafNode()

        self._advance_token()
        if self.current_token[2] != "identifier":
            pprint.pprint(self.parse_tree)
            raise Exception("11 " + str(self.current_token))
        self._addTokenLeafNode()

        self._advance_token()
        while self.current_token[2] == "symbol" and self.current_token[3] == "," and \
                (self.tokens[self.cur_token_index+1][2] == "keyword" or \
                self.tokens[self.cur_token_index+1][2] == "identifier") and \
                (self.tokens[self.cur_token_index+1][3] in ["int", "char", "boolean"] or \
                self.tokens[self.cur_token_index+1][2] == "identifier") and \
                self.tokens[self.cur_token_index+2][2] == "identifier":

            self._addTokenLeafNode()
            self._advance_token()
            self._addTokenLeafNode()
            self._advance_token()
            self._addTokenLeafNode()
            self._advance_token()

        self.current_node = self.current_node["parent"]
        self._reverse_token()


    def compileVarDec(self):
        self._advance_token()
        while self.current_token[2] == "keyword" and self.current_token[3] == "var":
            self.current_node["children"].append({
                "node_name": "varDec",
                "children": [],
                "parent": self.current_node,
            })
            self.current_node = self.current_node["children"][-1]
            self._addTokenLeafNode()

            self._advance_token()
            if self.current_token[2] != "keyword" and \
                    self.current_token[2] != "identifier":
                pprint.pprint(self.parse_tree)
                raise Exception("12 " + str(self.current_token))
            if self.current_token[2] == "keyword" and \
                    self.current_token[3] not in ["int", "char", "boolean"]:
                pprint.pprint(self.parse_tree)
                raise Exception("13 " + str(self.current_token))
            self._addTokenLeafNode()

            self._advance_token()
            if self.current_token[2] != "identifier":
                pprint.pprint(self.parse_tree)
                raise Exception("14 " + str(self.current_token))
            self._addTokenLeafNode()

            self._advance_token()
            while self.current_token[2] == "symbol" and self.current_token[3] == "," and \
                    self.tokens[self.cur_token_index+1][2] == "identifier":
                self._addTokenLeafNode()
                self._advance_token()
                self._addTokenLeafNode()
                self._advance_token()

            if self.current_token[2] != "symbol" or self.current_token[3] != ";":
                pprint.pprint(self.parse_tree)
                raise Exception("15 " + str(self.current_token))
            self._addTokenLeafNode()

            self.current_node = self.current_node["parent"]
            self._advance_token()


    def compileStatements(self):
        self.current_node["children"].append({
            "node_name": "statements",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]

        self._advance_token()

        if not (self.current_token[2] == "keyword" and self.current_token[3] in ["do", "let", "while", "if", "return"]):
            self.current_node = self.current_node["parent"]
            return

        while self.current_token[2] == "keyword" and self.current_token[3] in ["do", "let", "while", "if", "return"]:
            if self.current_token[3] == "do":
                self.compileDo()
            elif self.current_token[3] == "let":
                self.compileLet()
            elif self.current_token[3] == "while":
                self.compileWhile()
            elif self.current_token[3] == "if":
                self.compileIf()
            elif self.current_token[3] == "return":
                self.compileReturn()
        
        self.current_node = self.current_node["parent"]

    def compileDo(self):
        if self.current_token[2] != "keyword" or self.current_token[3] != "do":
            pprint.pprint(self.parse_tree)
            raise Exception("21 " + str(self.current_token))

        self.current_node["children"].append({
            "node_name": "doStatement",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]
        
        self._addTokenLeafNode()
        self._advance_token()
        self.compileSubroutineCall()

        if self.current_token[2] != "symbol" or self.current_token[3] != ";":
            pprint.pprint(self.parse_tree)
            raise Exception("22 " + str(self.current_token))
        self._addTokenLeafNode()

        self.current_node = self.current_node["parent"]
        self._advance_token()

    def compileLet(self):
        if self.current_token[2] != "keyword" or self.current_token[3] != "let":
            pprint.pprint(self.parse_tree)
            raise Exception("23 " + str(self.current_token))

        self.current_node["children"].append({
            "node_name": "letStatement",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]

        self._addTokenLeafNode()
        self._advance_token()
        
        if self.current_token[2] != "identifier":
            pprint.pprint(self.parse_tree)
            raise Exception("24 " + str(self.current_token))
        self._addTokenLeafNode()
        
        self._advance_token()
        if self.current_token[2] == "symbol" and self.current_token[3] == "[":
            self._addTokenLeafNode()
            self.compileExpression()
            if self.current_token[2] != "symbol" or self.current_token[3] != "]":
                pprint.pprint(self.parse_tree)
                raise Exception("25 " + str(self.current_token))
            self._addTokenLeafNode()
            self._advance_token()
            
        if self.current_token[2] != "symbol" or self.current_token[3] != "=":
            pprint.pprint(self.parse_tree)
            raise Exception("26 " + str(self.current_token))
        self._addTokenLeafNode()

        self.compileExpression()
        
        if self.current_token[2] != "symbol" or self.current_token[3] != ";":
            pprint.pprint(self.parse_tree)
            raise Exception("27 " + str(self.current_token))
        self._addTokenLeafNode()

        self.current_node = self.current_node["parent"]
        self._advance_token()

    def compileWhile(self):
        if self.current_token[2] != "keyword" or self.current_token[3] != "while":
            pprint.pprint(self.parse_tree)
            raise Exception("28 " + str(self.current_token))

        self.current_node["children"].append({
            "node_name": "whileStatement",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]

        self._addTokenLeafNode()
        
        self._advance_token()
        if self.current_token[2] != "symbol" or self.current_token[3] != "(":
            pprint.pprint(self.parse_tree)
            raise Exception("29 " + str(self.current_token))
        self._addTokenLeafNode()

        self.compileExpression()

        if self.current_token[2] != "symbol" or self.current_token[3] != ")":
            pprint.pprint(self.parse_tree)
            raise Exception("30 " + str(self.current_token))
        self._addTokenLeafNode()

        self._advance_token()
        if self.current_token[2] != "symbol" or self.current_token[3] != "{":
            pprint.pprint(self.parse_tree)
            raise Exception("31 " + str(self.current_token))
        self._addTokenLeafNode()

        self.compileStatements()
        
        if self.current_token[2] != "symbol" or self.current_token[3] != "}":
            pprint.pprint(self.parse_tree)
            raise Exception("32 " + str(self.current_token))
        self._addTokenLeafNode()

        self.current_node = self.current_node["parent"]
        self._advance_token()

    def compileReturn(self):
        if self.current_token[2] != "keyword" or self.current_token[3] != "return":
            pprint.pprint(self.parse_tree)
            raise Exception("21b " + str(self.current_token))

        self.current_node["children"].append({
            "node_name": "returnStatement",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]
        
        self._addTokenLeafNode()
        # self._advance_token()
        self.compileExpression()

        if self.current_token[2] != "symbol" or self.current_token[3] != ";":
            pprint.pprint(self.parse_tree)
            raise Exception("22b " + str(self.current_token))
        self._addTokenLeafNode()

        self.current_node = self.current_node["parent"]
        self._advance_token()

    def compileIf(self):
        if self.current_token[2] != "keyword" or self.current_token[3] != "if":
            pprint.pprint(self.parse_tree)
            raise Exception("33 " + str(self.current_token))

        self.current_node["children"].append({
            "node_name": "ifStatement",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]

        self._addTokenLeafNode()
        
        self._advance_token()
        if self.current_token[2] != "symbol" or self.current_token[3] != "(":
            pprint.pprint(self.parse_tree)
            raise Exception("34 " + str(self.current_token))
        self._addTokenLeafNode()

        self.compileExpression()

        if self.current_token[2] != "symbol" or self.current_token[3] != ")":
            pprint.pprint(self.parse_tree)
            raise Exception("35 " + str(self.current_token))
        self._addTokenLeafNode()

        self._advance_token()
        if self.current_token[2] != "symbol" or self.current_token[3] != "{":
            pprint.pprint(self.parse_tree)
            raise Exception("36 " + str(self.current_token))
        self._addTokenLeafNode()

        self.compileStatements()
        
        if self.current_token[2] != "symbol" or self.current_token[3] != "}":
            pprint.pprint(self.parse_tree)
            raise Exception("37 " + str(self.current_token))
        self._addTokenLeafNode()

        self._advance_token()
        if self.current_token[2] != "keyword" or self.current_token[3] != "else":
            self.current_node = self.current_node["parent"]
            return
        self._addTokenLeafNode()

        self._advance_token()
        if self.current_token[2] != "symbol" or self.current_token[3] != "{":
            pprint.pprint(self.parse_tree)
            raise Exception("36 " + str(self.current_token))
        self._addTokenLeafNode()

        self.compileStatements()
        
        if self.current_token[2] != "symbol" or self.current_token[3] != "}":
            pprint.pprint(self.parse_tree)
            raise Exception("37 " + str(self.current_token))
        self._addTokenLeafNode()

        self.current_node = self.current_node["parent"]
        self._advance_token()

    def compileExpression(self):
        self.current_node["children"].append({
            "node_name": "expression",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]

        self._advance_token()
        if (self.current_token[2] != "integerConstant" and \
                self.current_token[2] != "stringConstant" and \
                self.current_token[2] != "keyword" and \
                self.current_token[2] != "identifier" and \
                self.current_token[2] != "symbol" and \
                self.current_token[3] not in ["null", "true", "false", "this", "(", "-", "~"]) or \
                (self.current_token[2] == "symbol" and self.current_token[3] not in ["null", "true", "false", "this", "(", "-", "~"]):
            # self._reverse_token()
            self.current_node = self.current_node["parent"]
            self.current_node["children"].pop()
            return
        
        self._reverse_token()
        self.compileTerm()

        while self.current_token[2] == "symbol" and self.current_token[3] in ["+", "-", "*", "/", "&", "|", ">", "<", '=']:
            self._addTokenLeafNode()
            self.compileTerm()
        
        self.current_node = self.current_node["parent"]

    def compileTerm(self):
        self._advance_token()
        if (self.current_token[2] != "integerConstant" and \
                self.current_token[2] != "stringConstant" and \
                self.current_token[2] != "keyword" and \
                self.current_token[2] != "identifier" and \
                self.current_token[2] != "symbol" and \
                self.current_token[3] not in ["null", "true", "false", "this", "(", "-", "~"]) or \
                (self.current_token[2] == "symbol" and self.current_token[3] not in ["null", "true", "false", "this", "(", "-", "~"]):
            pprint.pprint(self.parse_tree)
            raise Exception("20 " + str(self.current_token))

        self.current_node["children"].append({
            "node_name": "term",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]

        if self.current_token[2] == "integerConstant" or self.current_token[2] == "stringConstant" or \
                (self.current_token[2] == "keyword" and self.current_token[3] in ["null", "true", "false", "this"]) or \
                (self.current_token[2] == "identifier" and self.tokens[self.cur_token_index+1][3] not in ["[", ".", "("]):
            self._addTokenLeafNode()
            self._advance_token()
            self.current_node = self.current_node["parent"]
            return

        if self.current_token[2] == "identifier" and self.tokens[self.cur_token_index+1][2] == "symbol" and \
                self.tokens[self.cur_token_index+1][3] == "[":
            self._addTokenLeafNode()
            self._advance_token()
            self._addTokenLeafNode()
            self.compileExpression()
            if self.current_token[2] != "symbol" or \
                    self.current_token[3] != "]":
                pprint.pprint(self.parse_tree)
                raise Exception("16 " + str(self.current_token))
            self._addTokenLeafNode()
            self._advance_token()
            self.current_node = self.current_node["parent"]
            return

        if (self.current_token[2] == "identifier" and self.tokens[self.cur_token_index+1][2] == "symbol" and \
                self.tokens[self.cur_token_index+1][3] == "(") or \
                (self.current_token[2] == "identifier" and self.tokens[self.cur_token_index+1][2] == "symbol" and \
                self.tokens[self.cur_token_index+1][3] == "."):
            self.compileSubroutineCall()
            self.current_node = self.current_node["parent"]
            return

        if self.current_token[2] == "symbol" and self.current_token[3] == "(":
            self._addTokenLeafNode()
            # self._reverse_token()
            self.compileExpression()
            if self.current_token[2] != "symbol" or self.current_token[3] != ")":
                pprint.pprint(self.parse_tree)
                raise Exception("19 " + str(self.current_token))
            self._addTokenLeafNode()
            self._advance_token()
            self.current_node = self.current_node["parent"]
            return

        if self.current_token[2] == "symbol" and self.current_token[3] in ["-", "~"]:
            self._addTokenLeafNode()
            self.compileTerm()
            self.current_node = self.current_node["parent"]
            return
            
            
    def compileSubroutineCall(self):
        if not (self.current_token[2] == "identifier" and self.tokens[self.cur_token_index+1][2] == "symbol" and \
                self.tokens[self.cur_token_index+1][3] == "(") and \
                not (self.current_token[2] == "identifier" and self.tokens[self.cur_token_index+1][2] == "symbol" and \
                self.tokens[self.cur_token_index+1][3] == "."):
            pprint.pprint(self.parse_tree)
            raise Exception("17 " + str(self.current_token))
        
        if self.current_token[2] == "identifier" and self.tokens[self.cur_token_index+1][2] == "symbol" and \
                self.tokens[self.cur_token_index+1][3] == ".":
            self._addTokenLeafNode()
            self._advance_token()
            self._addTokenLeafNode()
            self._advance_token()
            self.compileSubroutineCall()

        if self.current_token[2] == "identifier" and self.tokens[self.cur_token_index+1][2] == "symbol" and \
                self.tokens[self.cur_token_index+1][3] == "(":
            self._addTokenLeafNode()
            self._advance_token()
            self._addTokenLeafNode()
            self.compileExpressionList()
            if self.current_token[2] != "symbol" or self.current_token[3] != ")":
                pprint.pprint(self.parse_tree)
                raise Exception("18 " + str(self.current_token))
            self._addTokenLeafNode()
            self._advance_token()

    def compileExpressionList(self):
        self.current_node["children"].append({
            "node_name": "expressionList",
            "children": [],
            "parent": self.current_node,
        })
        self.current_node = self.current_node["children"][-1]

        self.compileExpression()

        if self.current_token[2] == "symbol" and self.current_token[3] == ",":
            while self.current_token[2] == "symbol" and self.current_token[3] == ",":
                self._addTokenLeafNode()
                self.compileExpression()
        
        self.current_node = self.current_node["parent"]


    def _addTokenLeafNode(self):
        self.current_node["children"].append({
            "node_name": self.current_token[2],
            "children": self.current_token[3],
            "parent": self.current_node,
        })
    
    def writeOutputXmlFile(self, node, indent=0):
        if isinstance(node["children"], str):
            node_child = node["children"]
            safe_chars = {
                ">": "&gt;",
                "<": "&lt;",
                "&": "&amp;",
            }
        
            if node_child in ["<", ">", "&"]:
                node_child = safe_chars[node_child]
            
            [self.output_file.write("  ") for _ in range(0, indent)]
            self.output_file.write("<" + node["node_name"] + "> ")
            self.output_file.write(node_child)
            self.output_file.write(" </" + node["node_name"] + ">\n")
        
            return
        
        [self.output_file.write("  ") for _ in range(0, indent)]
        self.output_file.write("<" + node["node_name"] + ">\n")

        for child_node in node["children"]:
            self.writeOutputXmlFile(child_node, indent+1)
        
        [self.output_file.write("  ") for _ in range(0, indent)]
        self.output_file.write("</" + node["node_name"] + ">\n")
    
    def traverse(self, node):
        print(node["node_name"] + ": ", end="")
        if isinstance(node["children"], str):
            print(node["children"])
            return
        else:
            for child_node in node["children"]:
                self.traverse(child_node)



