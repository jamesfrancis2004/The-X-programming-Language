import sys
import os
from Block import Block
from Scope import Scope
from From_Loop import From_Loop
from i32 import i32
from Function import Function
from Char import Char
from Println import Println
from Char_Array import Char_Array
from f32 import f32
import Constants


class Parser:

    def __init__(self, file_name):
        self.END_OF_LINE = ';'
        self.WHITESPACE = set(['\n', ' ', '\t'])
        self.LOGICAL_OPERATORS = set(["+", "*", "-", "/",
                                     "<", ">", "^", "&",
                                     "%" ])

        self._functions = {"operation": self.parse_operation,
                           "struct": self.parse_struct, 
                           "i32": self.parse_i32, 
                           "char[]": self.parse_char_array,
                           "f32": self.parse_f32,
                           "f64": self.parse_f64,
                           "println": self.parse_println,
                           "char": self.parse_char,
                           "loop": self.parse_loop}


        self.variable_bit_conversion = {"char": 8} 
        self.raw_code = self.read_file(file_name)
        self.global_scope = Scope({}, True)
        self.global_scope.built_ins = set([])
        self.global_block = None
        self.idx = 0

    def return_malloced_array(self, text, scope):
        text_list = text.split("[")
        if text_list[0] not in scope.valid_var_types:
            print(f"Error {text_list[0]} is an invalid variable")
            exit()

        size = ""
        for i in text_list[1]:
            if i in Constants.NUMBERS:
                size += i
            elif i == "]":
                break
            else:
                print(f"{text} is an invalid variable declaration")
        bit_size= self.variable_bit_conversion[text_list[0]]
        return f"malloc({bit_size} * {size})"
            
    def check_valid_variable_name(self, variable_name):
        for i in variable_name:
            if i not in Constants.VALID_VAR_CHARS:
                print(f"{variable_name} is an invalid variable name")
                exit()

    def check_integer_arithemetic(self, variable_name, decl, scope):
        for i in decl[2:len(decl)]:
            if i in scope.variables:
                variable = scope.variables[i]
                if variable.type == "i32":
                    continue
                elif variable.type == "f32":
                    continue
                elif variable.type == "f64":
                    continue
                else:
                    print("Operation with type {variable.type} is incompatible with i32 {variable_name}")
                    exit()
            else:
                for j in i:
                    if j not in Constants.VALID_INT_SYMBOLS:
                        print(f"{j} is an invalid symbol for declaration of i32 {variable_name}")
                        exit()

        return " ".join(decl)


    def parse_from_loop(self, variable_name, text_to_parse, scope):
        self.check_valid_variable_name(variable_name)
        to_index = -1
        for idx, i in enumerate(text_to_parse):
            if i == "to":
                to_index = idx
                break

        if to_index == -1:
            print(f"Missing 'to' in loop {' '.join(text_to_parse)}")
            exit()

        start = self.check_integer_arithemetic(variable_name, text_to_parse[0:to_index], scope)
        by_index = -1
        
        for count, i in enumerate(text_to_parse[to_index+1:len(text_to_parse)]):
            if i == "by":            
                by_index = count + (to_index+1)
                break

        if by_index == -1:
            end = self.check_integer_arithemetic("from loop end arg",
                    text_to_parse[to_index+1:len(text_to_parse)], scope)
            step = 1
        else:
            end = self.check_integer_arithemetic("from loop end",
                    text_to_parse[to_index+1 : by_index], scope)
            step = self.check_integer_arithemetic("from loop step",
                    text_to_parse[by_index+1:len(text_to_parse)], scope)

        new_var = i32(variable_name, None)
        new_var.index += 1
        new_from_loop = From_Loop(variable_name, start, end, step, Scope({new_var.name: new_var}))
        scope.body.append(new_from_loop)
        return new_from_loop.scope

    def parse_loop(self, text_to_parse, scope):
        if len(text_to_parse) > 8:
            print(f"{' '.join(text_to_parse)} is an invalid from declaration")
            exit()

        if text_to_parse[1] == "from":
            new_scope = self.parse_from_loop(text_to_parse[0], text_to_parse[2:len(text_to_parse)], scope)
        else:
            print(f"{' '.join(text_to_parse)} is an invalid loop declaration")
            exit()

        return new_scope

    def parse_operation(self, title, scope, redeclare=False):
        if len(title) < 2:
            print(f"{' '.join(title)} is an invalid operation declaration")
            exit()

        variable_name = title[0]
        self.check_valid_variable_name(variable_name)
        op_parameters = title[1]
        if op_parameters[0] != "(":
            print(f"Expected a '(' when declaring {variable_name} parameters")
            exit()

        if op_parameters[len(op_parameters) - 1] != ")":
            print(f"Expected a ) to close {variable_name} parameters")
            exit()
        
        parameter_list = [i.split() for i in op_parameters[1:len(op_parameters) - 1].split(",")]
        if redeclare:
            declared_parameters = list(scope.variables[variable_name].scope.parameters.values())
            parameter_list = op_parameters[1:len(op_parameters) - 1].replace(" ", "").split(",")
            variables_string = ""
            for idx, i in enumerate(parameter_list):
                if len(i) == 0:
                    break
                elif i in scope.variables:
                    variable = scope.variables[i]
                    if variable.type == declared_parameters[idx].type:
                        if idx == 0:
                            variables_string += variable.name
                        else:
                            variables_string += f", {variable.name}"
                        continue
                    else:
                        print("{variable.name} is a different type to original variable declared {declared_parameters[idx].name}")
                        exit()

                else:
                    print(f"{i} is an undeclared variable in current scope")
                    exit()
            var = scope.variables[variable_name]
            var.variables.append(variables_string)
            scope.body.append(var)
        else:
                parameters = {}
                for i in parameter_list:
                    if len(i) == 0:
                        break
                    if i[0] not in scope.valid_var_types:
                        print(f"{i[0]} is an invalid variable type")
                        exit()
                    else:
                        if i[0] == "i32":
                            new_var = i32(i[1], i[1])
                            parameters.update({new_var.name: new_var})
                            new_var.index += 1
                        

                new_scope = Scope(parameters)
                variables = ""
                for idx, i in enumerate(new_scope.parameters.values()):
                    if idx == 0:
                        variables += f"{Constants.TYPE_CONVERSION[i.type]} {i.name}"
                    else:
                        variables += f",{Constants.TYPE_CONVERSION[i.type]} {i.name}"

                    
                new_function = Function(variable_name, None, new_scope, variables)
                scope.variables.update({new_function.name : new_function}) 
                scope.body.append(new_function)
                return new_function.scope


    def parse_struct(self, title, scope):
        pass
             

    def parse_char(self, text_to_parse, scope):
        if len(text_to_parse) < 3:
            print(f"{' '.join(text_to_parse)} declaration for type char")
            exit()

        variable_name = text_to_parse[0]
        self.check_valid_variable_name(variable_name)
        if text_to_parse[1] != "=":
            print(f"Expected a '=' when declaring {variable_name}")
            exit()

        if text_to_parse[2][0] == "'":
            if text_to_parse[2][len(text_to_parse) - 1] == "'":
                if (len(text_to_parse[2]) - 1) - 1 == 1:
                    char = ''.join(text_to_parse[2])
                elif (len(text_to_parse[2]) - 1) - 1 == 2 and text_to_parse[2][1] == '\\':
                    char = ''.join(text_to_parse[2])
                else:
                    print(f"{text_to_parse} is an invalid character declaration for variable {variable_name}")
                    exit()
            else:
                print(f"Expected a  \"'\" to end the char {variable_name}")
                exit()
        else:
            print("Expected a \"'\" to start the variable declaration of char {variable_name}")
            exit()

        new_char = Char(variable_name, char)
        scope.variables.update({f"{new_char.name}" : new_char})
        scope.body.append(new_char)


    def parse_i32(self, decl, scope, redeclare=False):
        if len(decl) < 3:
            print(f"{' '.join(decl)} is an invalid variable declaration")
            exit()

        variable_name = decl[0]
        self.check_valid_variable_name(variable_name)

        if decl[1] != "=":
            print(f"Expected a '=' when declaring {variable_name}")
            exit()

        declaration_text = self.check_integer_arithemetic(variable_name, decl[2:len(decl)], scope)
        if redeclare:
            scope.variables[variable_name].redeclare_variable(declaration_text)
            scope.body.append(scope.variables[variable_name])
        else:
            new_int = i32(variable_name, declaration_text)
            scope.variables.update({f"{new_int.name}" : new_int})
            scope.body.append(new_int)

    def parse_println(self, text_to_parse, scope):
            if len(text_to_parse) < 1:
                print(f"{' '.join(text_to_parse)} is an invalid argument to function println")
                exit()

            new_print = Println()
            for i in text_to_parse:
                if i[0] == '"':
                    if i[len(i) - 1] != '"':
                        print("""Expected a '"'  to close """ + text_to_parse)
                        exit()
                    else:
                        new_print.text.append(i[1:len(i) - 1])

                else:
                    if i in scope.variables:
                        new_print.update_variable(scope.variables[i])
                    else:
                        print(f"{i} is an invalid variable. Pass an existing variable to println")
                        exit()

            scope.body.append(new_print)

    def parse_char_array(self, text_to_parse, scope):
        if len(text_to_parse) > 5:
            print(f"{' '.join(text_to_parse)} is an invalid declaration of char[]")
            exit()

        variable_name = text_to_parse[0]
        self.check_valid_variable_name(variable_name)
        
        if text_to_parse[1] != "=":
            print(f"Expected a '=' when declaring {variable_name}")
            exit()

        if text_to_parse[2] == "new":
            declaration_text = self.return_malloced_array(text_to_parse[3], scope)


        else:
            if text_to_parse[2][0] == '"' and text_to_parse[2][len(text_to_parse[2]) - 1] == '"':
                declaration_text = "".join(text_to_parse[2])
            else:
                print(f"{' '.join(text_to_parse)} is an invalid declaration of char[]")
                exit()

        new_char_array = Char_Array(variable_name, declaration_text)
        scope.variables.update({new_char_array.name: new_char_array})
        scope.body.append(new_char_array)

    def parse_f32(self, decl, scope, redeclare=False):
        if len(decl) < 3:
            print(f"{' '.join(decl)} is an invalid variable declaration")
            exit()

        variable_name = decl[0]
        self.check_valid_variable_name(variable_name)

        if decl[1] != "=":
            print(f"Expected a '=' when declaring {variable_name}")
            exit()

        for i in decl[2:len(decl)]:
            if i in scope.variables:
                variable = scope.variables[i]
                if variable.type == "f32":
                    continue
                elif variable.type == "f64":
                    continue
                elif variable.type == "i32":
                    print(f"Adding type i32 {variable.name} to type f32 may cause a loss in precision. Consider casting to f32")
                    continue
                else:
                    print(f"Incompatible operation for type {variable.type} {variable.name} with f32 {variable_name}")
                    exit()
            elif i[0] in Constants.LOGICAL_OPERATORS:
                pass
            else:
                found_dot_point = False
                for j in i:
                    if j == ".":
                        found_dot_point = True
                    elif j == "." and found_dot_point:
                        print(f'Too many ".." when declaring float')
                        exit()
                    if j not in Constants.VALID_FLOAT_SYMBOLS:
                        print(f"{j} is an invalid symbol for declaration of f32 {variable_name}")
                        exit()

                if not found_dot_point:
                    i.extend(list(".0"))

        declaration_text = " ".join(decl[2:len(decl)])
        if redeclare:
            scope.variables[variable_name].redeclare_variable(declaration_text)
            scope.body.append(scope.variables[variable_name])
        else:
            new_f32 = f32(variable_name, declaration_text)
            scope.variables.update({f"{new_f32.name}" : new_f32})
            scope.body.append(new_f32)

    def parse_f64(self, string):
        print(string)
    

 

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
                    self._functions[i[0]](i[1:len(i)], scope)
                elif i[0] in scope.variables:
                    var_type = scope.variables[i[0]].type
                    self._functions[var_type](i, scope, redeclare=True)

                else:
                    print(" ".join(i) + " is an an invalid variable declaration")
                    exit()

            if isinstance(i, Block):
                if i.title_text[0] in scope.valid_var_types:
                    new_scope = self._functions[i.title_text[0]](i.title_text[1:len(i.title_text)], scope)
                    new_scope.variables.update(scope.variables)
                    new_scope.valid_var_types.update(scope.valid_var_types)
                    self.translate_tokens(i.body, new_scope)

                    









file_name = f"{sys.argv[1]}.x"        
parser = Parser(file_name)
parser.tokenize_by_block([])
parser.translate_tokens(parser.global_block, parser.global_scope)
with open(f"src/{sys.argv[1]}.c", "w") as fp:
    fp.write("#include <stdio.h>\n#include <stdlib.h>\n")
    fp.write(parser.global_scope.return_string())



