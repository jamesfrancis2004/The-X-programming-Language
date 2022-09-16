import sys
from Block import Block
from Scope import Scope


class Parser:

    def __init__(self, file_name):
        self.END_OF_LINE = ';'
        self.WHITESPACE = set(['\n', ' ', '\t'])
        self.LOGICAL_OPERATORS = set(["+", "*", "-", "/",
                                     "<", ">", "^", "&",
                                     "%" ])
        
        self.raw_code = self.read_file(file_name)
        self.global_scope = Scope({})
        self.global_scope.built_ins = set([])
        self.variables = {}
        self.global_block = None
        self.idx = 0

    def read_file(self, file_name):
        try:
            fp = open(file_name, "r")
            file_contents = fp.read()
            fp.close()
        except FileNotFoundError:
            print(f"{file_name} is a non existent file", file=sys.stderr)
            exit()

        return file_contents

    def tokenize_by_block(self, tokens):
        line_token = []
        curr_token = []
        while self.idx < len(self.raw_code):
            char_tok = self.raw_code[self.idx]
            if char_tok in self.WHITESPACE:
                if len(curr_token) != 0:
                    line_token.append("".join(curr_token))
                    curr_token = []

                self.idx += 1

            elif char_tok in self.LOGICAL_OPERATORS:
                if (len(curr_token) != 0):
                    line_token.append("".join(curr_token))
                    curr_token = []
                
                while self.raw_code[self.idx] in self.LOGICAL_OPERATORS:
                    curr_token += self.raw_code[self.idx]
                    self.idx += 1

                line_token.append("".join(curr_token))
                curr_token = []
                self.idx += 1

            elif char_tok == ";":
                if (len(curr_token) != 0):
                    line_token.append("".join(curr_token))
                    curr_token = []

                tokens.append(line_token)
                line_token = []
                self.idx += 1

            elif char_tok == "{":
                if len(curr_token) != 0:
                    line_token.append("".join(curr_token))
                    curr_token = []
                
                new_scope = Block(line_token, [])
                line_token = []
                self.idx += 1
                self.tokenize_by_block(new_scope.body)
                tokens.append(new_scope)
                

           
            elif char_tok == "}":
                if len(curr_token) != 0:
                    line_token.append("".join(curr_token))

                if len(line_token) != 0: 
                    tokens.append(line_token)

                curr_token = []
                line_token = []
                self.idx += 1
                return

            elif char_tok == "(":
                if len(curr_token) != 0:
                    line_token.append("".join(curr_token))
                    curr_token = []


                while (self.raw_code[self.idx] != ")"):
                    curr_token += self.raw_code[self.idx]
                    self.idx += 1

                curr_token += self.raw_code[self.idx]
                self.idx += 1
                line_token.append("".join(curr_token))
                curr_token = []

            elif char_tok == '"':
                if len(curr_token) != 0:
                    line_token.append("".join(curr_token))
                    curr_token = []
                curr_token += char_tok
                self.idx += 1
                while (self.raw_code[self.idx] != '"'):
                        curr_token += self.raw_code[self.idx]
                        self.idx += 1

                curr_token += self.raw_code[self.idx]
                self.idx += 1
                line_token.append("".join(curr_token))
                curr_token = []

 
            else:
                curr_token += char_tok
                self.idx += 1

        self.global_block = tokens


    def analyse_line(self, line):
        pass


    def translate_tokens(self, args, scope):
        for i in args:
            if isinstance(i, list):
                if i[0] in scope.valid_var_types or i[0] in scope.built_ins:
                    scope._functions[i[0]](i[1:len(i)])
                elif i[0] in scope.variables:
                    var_type = scope.variables[i[0]].type
                    scope._functions[var_type](i, redeclare=True)


                else:
                    print(" ".join(i) + " is an an invalid variable declaration")
                    exit()

            if isinstance(i, Block):
                if i.title_text[0] in scope.valid_var_types:
                    new_scope = scope._functions[i.title_text[0]](i.title_text[1:len(i.title_text)])
                    new_scope.variables.update(scope.variables)
                    new_scope.valid_var_types.update(scope.valid_var_types)
                    self.translate_tokens(i.body, new_scope)

                    









file_name = "test.x"        
parser = Parser(file_name)
parser.tokenize_by_block([])
parser.translate_tokens(parser.global_block, parser.global_scope)
with open("src/test.c", "w") as fp:
    fp.write("#include <stdio.h>\n#include <stdlib.h>\n")
    fp.write(parser.global_scope.return_string())



