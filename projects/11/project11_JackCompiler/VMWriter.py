# ##############################################################################
# //////////////////////////////////////////////////////////////////////////////
# 
# DISCLAIMER FROM THE AUTHOR
# Be warned, the code quality below is identical to a metastasized tumor.
# 
# //////////////////////////////////////////////////////////////////////////////
# ##############################################################################

import copy
import uuid

class VMWriter:

    def __init__(self, parse_tree, symbolTable, input_file_url):
        self.parse_tree = copy.deepcopy(parse_tree)
        self.symbolTable = symbolTable
        self.vm_statements = []

        self.current_subroutine_kind = ""
        self.current_subroutine_return_type = ""
        self.current_subroutine_name = ""
        
        self.traverse(self.parse_tree)

        self.output_file_url = input_file_url.split(".")
        
        if self.output_file_url[-1] == "jack":
            self.output_file_url.pop()
        
        self.output_file_url.append("vm")
        self.output_file_url = ".".join(self.output_file_url)
        self.output_file = open(self.output_file_url, "w")
        self.writeOutputVMFile()
        self.output_file.close()

        # for x in self.vm_statements:
        #     print(x)


    def traverse(self, node):
        if not isinstance(node, dict):
            return
        # if node["node_name"] == "expression":
        #     self.expressionWrite(node["children"], 0)
        #     return
        if node["node_name"] == "subroutineDec":
            self.current_subroutine_kind = node["children"][0]["children"]
            self.current_subroutine_return_type = node["children"][1]["children"]
            self.current_subroutine_name = node["children"][2]["children"]
            self.vm_statements.append("// <-subroutineDec-> " + self.current_subroutine_name)
            vm_statement = "function " + self.symbolTable.class_name + \
                           "." + node["children"][2]["children"] + " " + \
                           str(self.symbolTable.varCount(node["children"][2]["children"]))
            self.vm_statements.append(vm_statement)
            if self.current_subroutine_kind == "constructor":
                self.constructorSubroutineDecWrite()
            if self.current_subroutine_kind == "method":
                self.methodSubroutineDecWrite()
        if node["node_name"] == "letStatement":
            self.vm_statements.append("// <-letStatement->")
            self.letStatementWrite(node["children"])
        if node["node_name"] == "doStatement":
            self.vm_statements.append("// <-doStatement->")
            self.doStatementWrite(node["children"])
        if node["node_name"] == "returnStatement":
            self.vm_statements.append("// <-returnStatement->")
            self.returnStatementWrite(node["children"])
        if node["node_name"] == "ifStatement":
            self.vm_statements.append("// <-ifStatement->")
            self.ifStatementWrite(node["children"])
            return
        if node["node_name"] == "whileStatement":
            self.vm_statements.append("// <-whileStatement->")
            self.whileStatementWrite(node["children"])
            return

        for child_node in node["children"]:
            self.traverse(child_node)

    def expressionWrite(self, token_list, cur_index):
        if len(token_list) < 0 or cur_index >= len(token_list):
            return

        binary_op = {
            "+": "add",
            "-": "sub",
            "*": "call Math.multiply 2",
            "/": "call Math.divide 2",
            "<": "lt",
            ">": "gt",
            "=": "eq",
            "&": "and",
            "|": "or",
        }

        if cur_index < len(token_list) and token_list[cur_index]["node_name"] == "term":
            self.termWrite(token_list[cur_index])
            return self.expressionWrite(token_list, cur_index+1)
        
        if cur_index < len(token_list)-1 and token_list[cur_index]["node_name"] == "symbol" and \
                token_list[cur_index]["children"] in binary_op and token_list[cur_index+1]["node_name"] == "term":
            self.termWrite(token_list[cur_index+1])
            self.vm_statements.append(binary_op[token_list[cur_index]["children"]])
            return self.expressionWrite(token_list, cur_index+2)

    def termWrite(self, term):
        if len(term["children"]) == 1 and term["children"][0]["node_name"] == "integerConstant":
            self.vm_statements.append("push constant " + term["children"][0]["children"])
            return
        
        if len(term["children"]) == 1 and term["children"][0]["node_name"] == "stringConstant":
            self.stringConstantWrite(term["children"][0]["children"])
            return
        
        if len(term["children"]) == 1 and term["children"][0]["node_name"] == "keyword":
            if term["children"][0]["children"] == "this":
                self.vm_statements.append("push pointer 0")
            elif term["children"][0]["children"] in ["null", "false"]:
                self.vm_statements.append("push constant 0")
            elif term["children"][0]["children"] == "true":
                self.vm_statements.append("push constant 1")
                self.vm_statements.append("neg")
            return
        
        if len(term["children"]) == 1 and term["children"][0]["node_name"] == "identifier":
            ident_details = self.symbolTable.search(self.current_subroutine_name, term["children"][0]["children"])
            if ident_details is None:
                raise Exception("[3b] Unknown identifier '" + term["children"][0]["node_name"] + "'")
            self.vm_statements.append("push " + ident_details["segment"] + " " + str(ident_details["index"]))
            return
        
        if len(term["children"]) > 2 and term["children"][0]["node_name"] == "identifier" and \
                term["children"][1]["children"] == "[" and term["children"][2]["node_name"] == "expression":
            ident_details = self.symbolTable.search(self.current_subroutine_name, term["children"][0]["children"])
            if ident_details is None:
                raise Exception("[3b] Unknown identifier '" + term["children"][0]["node_name"] + "'")
            self.vm_statements.append("push " + ident_details["segment"] + " " + str(ident_details["index"]))
            self.expressionWrite(term["children"][2]["children"], 0)
            self.vm_statements.append("add")
            self.vm_statements.append("pop pointer 1")
            self.vm_statements.append("push that 0")
            return
       
        if len(term["children"]) > 2 and term["children"][0]["node_name"] == "identifier" and \
                term["children"][1]["children"] == "(" and term["children"][2]["node_name"] == "expressionList":
            self.subroutineCallWrite(term["children"], 1)
            return
       
        if len(term["children"]) > 4 and term["children"][0]["node_name"] == "identifier" and \
                term["children"][1]["children"] == "." and term["children"][2]["node_name"] == "identifier" and \
                term["children"][3]["children"] == "(" and term["children"][4]["node_name"] == "expressionList":
            self.subroutineCallWrite(term["children"], 3)
            return
        
        if len(term["children"]) > 2 and term["children"][0]["children"] == "(" and \
                term["children"][1]["node_name"] == "expression" and term["children"][2]["children"] == ")":
            self.expressionWrite(term["children"][1]["children"], 0)
            return
        
        if len(term["children"]) > 1 and term["children"][0]["children"] in ["-", "~"] and \
                term["children"][1]["node_name"] == "term":
            self.termWrite(term["children"][1])
            unary_op = {
                "-": "neg",
                "~": "not",
            }
            self.vm_statements.append(unary_op[term["children"][0]["children"]])
            return

        
        

        
    def subroutineCallWrite(self, token_list, cur_index):
        subroutine_name = token_list[cur_index-1]["children"]
        subroutine_prefix = ""

        subroutine_type = ""
        num_of_args = 0
        if token_list[cur_index-2]["children"] == "." and \
                token_list[cur_index-3]["node_name"] == "identifier":
            subroutine_prefix = token_list[cur_index-3]["children"]
            if subroutine_prefix[0].isupper():
                subroutine_type = "function"
            elif subroutine_prefix[0].islower():
                subroutine_type = "method"
                num_of_args += 1
        else:
            subroutine_type = "inClassMethod"
            num_of_args += 1
        
        if subroutine_type == "method":
            res = self.symbolTable.search(self.current_subroutine_name, subroutine_prefix)
            if res is None:
                raise Exception("[2] Unknown identifier or subroutine: '" + subroutine_prefix + "." + subroutine_name + "(...)")
            subroutine_prefix = res["data_type"]
            vm_statement = "push " + res["segment"] + " " + str(res["index"])
            self.vm_statements.append(vm_statement)
        
        if subroutine_type == "inClassMethod":
            subroutine_prefix = self.symbolTable.class_name
            vm_statement = "push pointer 0"
            self.vm_statements.append(vm_statement)

        for i in range (0, len(token_list[cur_index+1]["children"])):
            if token_list[cur_index+1]["children"][i]["node_name"] == "expression":
                num_of_args += 1
                self.expressionWrite(token_list[cur_index+1]["children"][i]["children"], 0)

        vm_statement = "call " + subroutine_prefix + "." + subroutine_name + " " + str(num_of_args)
        self.vm_statements.append(vm_statement)

    def letStatementWrite(self, token_list):
        if token_list[1]["node_name"] != "identifier":
            raise Exception("[3] expected identifier, found '" + token_list[1]["node_name"] + "'")
        if token_list[3]["node_name"] != "expression":
            raise Exception("[4] expected expression, found '" + token_list[3]["node_name"] + "'")

        ident_name = token_list[1]["children"]
        ident_details = self.symbolTable.search(self.current_subroutine_name, ident_name)
        if ident_details is None:
            raise Exception("[5] Unknown identifier '" + ident_name + "'")

        if token_list[2]["children"] != "[":
            self.expressionWrite(token_list[3]["children"], 0)
            vm_statement = "pop " + ident_details["segment"] + " " + str(ident_details["index"])
            self.vm_statements.append(vm_statement)
        elif token_list[2]["children"] == "[":
            if token_list[6]["node_name"] != "expression":
                raise Exception("[4a] expected expression, found '" + token_list[6]["node_name"] + "'")
            self.expressionWrite(token_list[6]["children"], 0)
            self.vm_statements.append("push " + ident_details["segment"] + " " + str(ident_details["index"]))
            self.expressionWrite(token_list[3]["children"], 0)
            self.vm_statements.append("add")
            self.vm_statements.append("pop pointer 1")
            self.vm_statements.append("pop that 0")
        

    def doStatementWrite(self, token_list):
        for i, token in enumerate(token_list):
            if token["node_name"] == "symbol" and token["children"] == "(":
                self.subroutineCallWrite(token_list, i)
                self.vm_statements.append("pop temp 0")
                return
        
        raise Exception("[6] Expected subroutine call, found none.")
        
    def returnStatementWrite(self, token_list):
        if token_list[1]["node_name"] == "expression":
            self.expressionWrite(token_list[1]["children"], 0)
        
        if self.current_subroutine_return_type == "void" and token_list[1]["children"] == ";":
            self.vm_statements.append("push constant 0")
        
        self.vm_statements.append("return")
    
    def ifStatementWrite(self, token_list):
        label1 = "if_label1_" + "".join(str(uuid.uuid4()).split("-"))
        label2 = "if_label2_" + "".join(str(uuid.uuid4()).split("-"))

        if token_list[2]["node_name"] != "expression":
            raise Exception("[7] Expected expression, found none.")
        
        self.expressionWrite(token_list[2]["children"], 0)
        
        self.vm_statements.append("not")
        self.vm_statements.append("if-goto " + label1)

        self.traverse(token_list[5])

        self.vm_statements.append("goto " + label2)
        self.vm_statements.append("label " + label1)
        
        if len(token_list) > 7 and token_list[7]["children"] == "else":
            self.traverse(token_list[9])

        self.vm_statements.append("label " + label2)
    
    def whileStatementWrite(self, token_list):
        label1 = "while_label1_" + "".join(str(uuid.uuid4()).split("-"))
        label2 = "while_label2_" + "".join(str(uuid.uuid4()).split("-"))

        if token_list[2]["node_name"] != "expression":
            raise Exception("[7] Expected expression, found none.")
        
        self.vm_statements.append("label " + label1)

        self.expressionWrite(token_list[2]["children"], 0)
        
        self.vm_statements.append("not")
        self.vm_statements.append("if-goto " + label2)

        self.traverse(token_list[5])

        self.vm_statements.append("goto " + label1)
        self.vm_statements.append("label " + label2)

    def constructorSubroutineDecWrite(self):
        self.vm_statements.append("push constant " + str(len(self.symbolTable.symbol_table["class_table"]["this"])))
        self.vm_statements.append("call Memory.alloc 1")
        self.vm_statements.append("pop pointer 0")
        
    def methodSubroutineDecWrite(self):
        self.vm_statements.append("push argument 0")
        self.vm_statements.append("pop pointer 0")

    def stringConstantWrite(self, chars):
        char_len = len(chars)
        self.vm_statements.append("push constant " + str(char_len))
        self.vm_statements.append("call String.new 1")
        for char in chars:
            self.vm_statements.append("push constant " + str(ord(char)))
            self.vm_statements.append("call String.appendChar 2")
        
    def writeOutputVMFile(self):
        self.output_file.write("\n".join(self.vm_statements))
        self.output_file.write("\n")


        