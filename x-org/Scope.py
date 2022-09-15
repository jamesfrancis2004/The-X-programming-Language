import Constants
from i32 import i32
from function import Function
from Println import Println


class Scope(object):
    def __init__(self, parameters):
        self.parameters = parameters
        self.valid_var_types = {"i32", "f32", "f64",
                                "operation", "struct"}
        self.built_ins = set(["println"])
        self._functions = {"operation": self.parse_operation,
                           "struct": self.parse_struct, 
                           "i32": self.parse_i32, 
                           "str": self.parse_str,
                           "f32": self.parse_f32,
                           "f64": self.parse_f64,
                           "println": self.parse_println}

        self._constructors = {"i32": i32}
        self.variables = self.parameters.copy()

        self.body = []

    def return_string(self):
        string = ""
        for i in self.body:
            string += i.return_string()
        
        return string

    def check_valid_variable_name(self, variable_name):
        for i in variable_name:
            if i not in Constants.VALID_VAR_CHARS:
                print(f"{variable_name} is an invalid variable name")
                exit()

    def parse_operation(self, title):
        if len(title) < 2:
            print(f"{' '.join(title)} is an invalid operation declaration")
            exit()

        variable_name = title[0]
        self.check_valid_variable_name(variable_name)
        op_parameters = title[1]
        if op_parameters[0] != "(":
            print(f"Expected a '(' when declaring {variable_name} parameters")
            exit()
        print(title)
        if op_parameters[len(op_parameters) - 1] != ")":
            print(f"Expected a ) to close {variable_name} parameters")
            exit()

        parameter_list = [i.split() for i in op_parameters[1:len(op_parameters) - 1].split(",")]
        parameters = {}
        for i in parameter_list:
            if len(i) == 0:
                break
            if i[0] not in self.valid_var_types:
                print(f"{i[0]} is an invalid variable type")
                exit()
            else:
                if i[0] == "i32":
                    new_var = i32(i[1], None)
                    parameters.update({new_var.name: new_var})


        new_function = Function(variable_name, None, Scope(parameters))
        self.variables.update({new_function.name : new_function}) 
        self.body.append(new_function)
        return new_function
            

    def parse_struct(self, title):
        pass

    def parse_i32(self, decl):
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
                pass
            else:
                for j in i:
                    if j not in Constants.VALID_INT_SYMBOLS:
                        print(f"{j} is an invalid symbol for declaration of i32 {variable_name}")
                        exit()

        declaration_text = " ".join(decl[2:len(decl)])
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






    def parse_str(self, string):
        print(string)

    def parse_f32(self, string):
        print(string)

    def parse_f64(self, string):
        print(string)
    


