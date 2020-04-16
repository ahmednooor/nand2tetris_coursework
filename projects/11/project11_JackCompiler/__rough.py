def expressionWrite(self, expression_terms, cur_index):
        if len(expression_terms) < 0 or cur_index >= len(expression_terms):
            return

        operator_statements = {
            "+": "add",
            "-": "sub",
            "*": "call Math.multiply 2",
            "/": "call Math.divide 2",
            "<": "lt",
            ">": "gt",
            "=": "eq",
            "~": "not",
            "&": "and",
            "|": "or",
        }

        if expression_terms[cur_index]["node_name"] == "expression" or \
                (expression_terms[cur_index]["node_name"] == "term" and \
                len(expression_terms[cur_index]["children"]) > 1):
            self.expressionWrite(expression_terms[cur_index]["children"], 0)
            # return

        if expression_terms[cur_index]["node_name"] == "symbol" and \
                expression_terms[cur_index]["children"] in "+-*/<>=~&|" and \
                cur_index > 0 and expression_terms[cur_index-1]["children"][0]["node_name"] == "identifier":
            vm_statement = operator_statements[expression_terms[cur_index]["children"]]
            self.expressionWrite(expression_terms, cur_index+1)
            self.vm_statements.append(vm_statement)
            return
        
        if expression_terms[cur_index]["node_name"] == "symbol" and \
                expression_terms[cur_index]["children"] == "(" and \
                cur_index > 0 and expression_terms[cur_index-1]["node_name"] == "identifier":
            self.subroutineCallWrite(expression_terms, cur_index)
            return

        if expression_terms[cur_index]["node_name"] == "symbol" and \
                expression_terms[cur_index]["children"] == "[" and \
                cur_index > 0 and expression_terms[cur_index-1]["node_name"] == "identifier":
            ident_details = self.symbolTable.search(self.current_subroutine_name, expression_terms[cur_index-1]["children"])
            if ident_details is None:
                raise Exception("[1a] Unknown identifier: '" + expression_terms[cur_index-1]["node_name"] + "'")
            self.vm_statements.append("push " + ident_details["segment"] + " " + str(ident_details["index"]))
            self.expressionWrite(expression_terms[cur_index+1]["children"], 0)
            self.vm_statements.append("add")
            self.vm_statements.append("pop pointer 1")
            self.vm_statements.append("push that 0")
            return
        
        if expression_terms[cur_index]["node_name"] == "term" and \
                len(expression_terms[cur_index]["children"]) == 1 and \
                expression_terms[cur_index]["children"][0]["node_name"] == "identifier":
            ident_details = self.symbolTable.search(self.current_subroutine_name, expression_terms[cur_index]["children"][0]["children"])
            if ident_details is None:
                raise Exception("[1] Unknown identifier: '" + expression_terms[cur_index]["children"][0]["children"] + "'")
            vm_statement = "push " + str(ident_details["segment"]) + " " + str(ident_details["index"])
            self.vm_statements.append(vm_statement)

        if expression_terms[cur_index]["node_name"] == "term" and \
                expression_terms[cur_index]["children"][0]["node_name"] == "integerConstant":
            vm_statement = "push constant " + expression_terms[cur_index]["children"][0]["children"]
            self.vm_statements.append(vm_statement)

        if expression_terms[cur_index]["node_name"] == "term" and \
                expression_terms[cur_index]["children"][0]["node_name"] == "stringConstant":
            self.stringConstantWrite(expression_terms[cur_index]["children"][0]["children"])
        
        if expression_terms[cur_index]["node_name"] == "term" and \
                expression_terms[cur_index]["children"][0]["node_name"] == "keyword" and \
                expression_terms[cur_index]["children"][0]["children"] == "true":
            vm_statement = "push constant 1"
            self.vm_statements.append(vm_statement)
            vm_statement = "neg"
            self.vm_statements.append(vm_statement)
        
        if expression_terms[cur_index]["node_name"] == "term" and \
                expression_terms[cur_index]["children"][0]["node_name"] == "keyword" and \
                expression_terms[cur_index]["children"][0]["children"] in ["false", "null"]:
            vm_statement = "push constant 0"
            self.vm_statements.append(vm_statement)
        
        if expression_terms[cur_index]["node_name"] == "term" and \
                expression_terms[cur_index]["children"][0]["node_name"] == "keyword" and \
                expression_terms[cur_index]["children"][0]["children"] == "this":
            vm_statement = "push pointer 0"
            self.vm_statements.append(vm_statement)
            
        self.expressionWrite(expression_terms, cur_index+1)