import copy
import pprint

class SymbolTable:

    def __init__(self, parse_tree):
        self.parse_tree = copy.deepcopy(parse_tree)
        self.class_name = self.parse_tree["children"][1]["children"]
        self.symbol_table = {
            "class_table": {
                "this": [],
                "static": [],
            },
            "subroutine_tables": {
                # "__subroutine__name__": { # template
                #     "argument": [],
                #     "local": [],
                # },
            }
        }

        self.traverse(self.parse_tree)
        # pprint.pprint(self.symbol_table)

    def traverse(self, node):
        if not isinstance(node, dict):
            return
        if node["node_name"] == "classVarDec":
            self.populate_class_table(node["children"])
        elif node["node_name"] == "subroutineDec":
            self.current_subroutine = node["children"][2]["children"]
            self.current_subroutine_kind = node["children"][0]["children"]
            self.symbol_table["subroutine_tables"][node["children"][2]["children"]] = {
                "argument": [],
                "local": [],
            }
            if node["children"][0] == "method":
                self.symbol_table["subroutine_tables"][node["children"][2]]["argument"].append({
                    "name": "this",
                    "data_type": self.class_name,
                })
        elif node["node_name"] == "parameterList":
            self.populate_subroutine_table_arguments(node["children"])
        elif node["node_name"] == "varDec":
            self.populate_subroutine_table_locals(node["children"])
        for child_node in node["children"]:
            self.traverse(child_node)

    def populate_class_table(self, token_list):
        if len(token_list) < 1:
            return

        segment = token_list[0]["children"]
        data_type = token_list[1]["children"]

        if segment == "field":
            segment = "this"

        symbol_tokens = token_list[2:]

        for token in symbol_tokens:
            if token["node_name"] == "identifier":
                self.symbol_table["class_table"][segment].append({
                    "name": token["children"],
                    "data_type": data_type,
                })

    def populate_subroutine_table_arguments(self, token_list):
        if len(token_list) < 1:
            return
        if self.current_subroutine_kind == "method":
            self.symbol_table["subroutine_tables"][self.current_subroutine]["argument"].append({
                "name": "this",
                "data_type": self.class_name,
            })
        i = 0
        while i < len(token_list):
            token = token_list[i]
            segment = "argument"
            data_type = token["children"]
            self.symbol_table["subroutine_tables"][self.current_subroutine][segment].append({
                "name": token_list[i+1]["children"],
                "data_type": data_type,
            })
            i += 3
        
    def populate_subroutine_table_locals(self, token_list):
        if len(token_list) < 1:
            return

        segment = "local"
        data_type = token_list[1]["children"]

        symbol_tokens = token_list[2:]

        for token in symbol_tokens:
            if token["node_name"] == "identifier":
                self.symbol_table["subroutine_tables"][self.current_subroutine][segment].append({
                    "name": token["children"],
                    "data_type": data_type,
                })
    
    def search(self, subroutine_name, name):
        for i, v in enumerate(self.symbol_table["class_table"]["this"]):
            if v["name"] == name:
                res =  copy.deepcopy(v)
                res["segment"] = "this"
                res["index"] = i
                return res
        
        for i, v in enumerate(self.symbol_table["class_table"]["static"]):
            if v["name"] == name:
                res =  copy.deepcopy(v)
                res["segment"] = "static"
                res["index"] = i
                return res
        
        for i, v in enumerate(self.symbol_table["subroutine_tables"][subroutine_name]["argument"]):
            if v["name"] == name:
                res =  copy.deepcopy(v)
                res["segment"] = "argument"
                res["index"] = i
                return res
        
        for i, v in enumerate(self.symbol_table["subroutine_tables"][subroutine_name]["local"]):
            if v["name"] == name:
                res =  copy.deepcopy(v)
                res["segment"] = "local"
                res["index"] = i
                return res

        return None
    
    def varCount(self, subroutine_name):
        if subroutine_name not in self.symbol_table["subroutine_tables"]:
            return None
        
        return len(self.symbol_table["subroutine_tables"][subroutine_name]["local"])


        