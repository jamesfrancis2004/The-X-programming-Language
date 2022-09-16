import Constants
from i32 import i32
from f32 import f32
from Function import Function
from Println import Println
from Char_Array import Char_Array
from Char import Char
from From_Loop import From_Loop


class Scope(object):
    def __init__(self, parameters):
        self.parameters = parameters
        self.valid_var_types = {"i32", "f32", "f64",
                                "operation", "struct", 
                                "char[]",
                                "char",
                                "loop"}
        self.built_ins = set(["println"])
        self._functions = {"operation": self.parse_operation,
                           "struct": self.parse_struct, 
                           "i32": self.parse_i32, 
                           "char[]": self.parse_char_array,
                           "f32": self.parse_f32,
                           "f64": self.parse_f64,
                           "println": self.parse_println,
                           "char": self.parse_char,
                           "loop": self.parse_loop}

        self.variable_conversion = {"char": 8}

        self._constructors = {"i32": i32}
        self.variables = self.parameters.copy()
        self.body = []


    def return_string(self):
        string = ""
        for i in self.body:
            string += i.return_string()
        
        return string

    def return_malloced_array(self, text):
        text_list = text.split("[")
        if text_list[0] not in self.valid_var_types:
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
        bit_size= self.variable_conversion[text_list[0]]
        return f"malloc({bit_size} * {size})"
            


    def check_valid_variable_name(self, variable_name):
        for i in variable_name:
            if i not in Constants.VALID_VAR_CHARS:
                print(f"{variable_name} is an invalid variable name")
                exit()

    def check_integer_arithemetic(self, variable_name, decl):
        for i in decl[2:len(decl)]:
            if i in self.variables:
                variable = self.variables[i]
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





    def parse_from_loop(self, variable_name, text_to_parse):
        self.check_valid_variable_name(variable_name)
        to_index = -1
        for idx, i in enumerate(text_to_parse):
            if i == "to":
                to_index = idx
                break

        if to_index == -1:
            print(f"Missing 'to' in loop {' '.join(text_to_parse)}")
            exit()

        start = self.check_integer_arithemetic(variable_name, text_to_parse[0:to_index])
        by_index = -1
        for idx, i in enumerate(text_to_parse[to_index+1:len(text_to_parse)]):
            if i == "by":
                by_index = idx
                break

        if by_index == -1:
            end = self.check_integer_arithemetic("from loop end arg",
                    text_to_parse[to_index+1:len(text_to_parse)])
            step = 1
        else:
            end = self.check_integer_arithemetic("from loop end",
                    text_to_parse[to_index+1: by_index])
            step = self.check_integer_arithemetic("from loop step",
                    text_to_parse[by_index+1:len(text_to_parse)])

        new_var = i32(variable_name, None)
        new_var.index += 1
        new_from_loop = From_Loop(variable_name, start, end, step, Scope({new_var.name: new_var}))
        self.body.append(new_from_loop)
        return new_from_loop.scope



    def parse_loop(self, text_to_parse):
        print("here")
        if len(text_to_parse) > 6:
            print(f"{' '.join(text_to_parse)} is an invalid from declaration")
            exit()

        if text_to_parse[1] == "from":
            new_scope = self.parse_from_loop(text_to_parse[0], text_to_parse[2:len(text_to_parse)])
        else:
            print(f"{' '.join(text_to_parse)} is an invalid loop declaration")
            exit()

        return new_scope




    def parse_operation(self, title, redeclare=False):
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
            declared_parameters = list(self.variables[variable_name].scope.parameters.values())
            parameter_list = op_parameters[1:len(op_parameters) - 1].replace(" ", "").split(",")
            variables_string = ""
            for idx, i in enumerate(parameter_list):
                if len(i) == 0:
                    break
                elif i in self.variables:
                    variable = self.variables[i]
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
            var = self.variables[variable_name]
            var.variables.append(variables_string)
            self.body.append(var)


        else:
            parameters = {}
            for i in parameter_list:
                if len(i) == 0:
                    break
                if i[0] not in self.valid_var_types:
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
            self.variables.update({new_function.name : new_function}) 
            self.body.append(new_function)
            return new_function.scope
            

    def parse_struct(self, title):
        pass

    def parse_char(self, text_to_parse):
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
        self.variables.update({f"{new_char.name}" : new_char})
        self.body.append(new_char)


    def parse_i32(self, decl, redeclare=False):
        if len(decl) < 3:
            print(f"{' '.join(decl)} is an invalid variable declaration")
            exit()

        variable_name = decl[0]
        self.check_valid_variable_name(variable_name)

        if decl[1] != "=":
            print(f"Expected a '=' when declaring {variable_name}")
            exit()

        declaration_text = self.check_integer_arithemetic(variable_name, decl[2:len(decl)])
        if redeclare:
            self.variables[variable_name].redeclare_variable(declaration_text)
            self.body.append(self.variables[variable_name])
        else:
            new_int = i32(variable_name, declaration_text)
            self.variables.update({f"{new_int.name}" : new_int})
            self.body.append(new_int)

    def parse_println(self, text_to_parse):
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
                if i in self.variables:
                    new_print.update_variable(self.variables[i])
                else:
                    print(f"{i} is an invalid variable. Pass an existing variable to println")
                    exit()

        self.body.append(new_print)


    def parse_char_array(self, text_to_parse):
        if len(text_to_parse) > 5:
            print(f"{' '.join(text_to_parse)} is an invalid declaration of char[]")
            exit()

        variable_name = text_to_parse[0]
        self.check_valid_variable_name(variable_name)
        
        if text_to_parse[1] != "=":
            print(f"Expected a '=' when declaring {variable_name}")
            exit()

        if text_to_parse[2] == "new":
            declaration_text = self.return_malloced_array(text_to_parse[3])


        else:
            if text_to_parse[2][0] == '"' and text_to_parse[2][len(text_to_parse[2]) - 1] == '"':
                declaration_text = "".join(text_to_parse[2])
            else:
                print(f"{' '.join(text_to_parse)} is an invalid declaration of char[]")
                exit()

        new_char_array = Char_Array(variable_name, declaration_text)
        self.variables.update({new_char_array.name: new_char_array})
        self.body.append(new_char_array)

    def parse_f32(self, decl, redeclare=False):
        if len(decl) < 3:
            print(f"{' '.join(decl)} is an invalid variable declaration")
            exit()

        variable_name = decl[0]
        self.check_valid_variable_name(variable_name)

        if decl[1] != "=":
            print(f"Expected a '=' when declaring {variable_name}")
            exit()

        for i in decl[2:len(decl)]:
            if i in self.variables:
                variable = self.variables[i]
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
            self.variables[variable_name].redeclare_variable(declaration_text)
            self.body.append(self.variables[variable_name])
        else:
            new_f32 = f32(variable_name, declaration_text)
            self.variables.update({f"{new_f32.name}" : new_f32})
            self.body.append(new_f32)


    def parse_f64(self, string):
        print(string)
    


