import time
import subprocess
import os
import sys

class Parser:
    def __init__(self, data, pos, args):
        self.keywords = {"print": self.perform_print,
                         "str": self.new_string,
                         "i32": self.new_int,
                         "f32": self.new_float32,
                         "f64": self.new_float64,
                         "println": self.perform_println,
                         "loop": self.perform_loop,
                         "if": self.perform_if,
                         "elseif": self.perform_elseif,
                         "operation": self.perform_operation}
        self.builtins = {"len(": self.return_length}
        self.variables = {}
        self.temp_variables = {}
        self.whitespace = {" ": 0,
                           "\n":0,
                           "\t":0,
                           }
        self.equality_operators = {">": 0, "<": 0,
                                   "=": 0}
        self.math_symbols = {"+": 0, "*": 0, "/": 0, "-":0,
                            "^":0, "|":0, "&":0, "<":0,
                            ">":0, " ":0,"\n":0, "\t":0,
                            "(":0, ")":0, "0" :0, "1": 0,
                            "2":0, "3":0, "4": 0, "5":0,
                            "6":0, "7":0, "8": 0, "9":0,
                            ".":0}

        self.float_numerals = {"0": 0, "1": 0, "2":0,
                               "3": 0, "4": 0, "5":0,
                               "6": 0, "7": 0, "8":0,
                               "8": 0, "9": 0, ".":0}

        self.string_type_conversion  = {"String": "%s",
                                 "Int": "%d",
                                 "Float32": "%f",
                                 "Char": "%c",
                                 "Float64": "%g"}

        self.type_conversion = {"i32": "int",
                                "f32": "float",
                                "f64": "double",
                                "char": "char"}

        self.valid_var_chars = {"a": 0, "b": 0, "c": 0,
                                "d": 0, "e": 0, "f": 0,
                                "g": 0, "h": 0, "i": 0,
                                "j": 0, "k": 0, "l": 0,
                                "m": 0, "n": 0, "p": 0,
                                "q": 0, "r": 0, "s": 0,
                                "t": 0, "u": 0, "v": 0,
                                "h": 0, "i": 0, "j": 0,
                                "k": 0, "l": 0, "m": 0,
                                "n": 0, "o": 0, "p": 0,
                                "q": 0, "r": 0, "s": 0,
                                "t": 0, "u": 0, "v": 0,
                                "w": 0, "r": 0, "x": 0,
                                "y": 0, "z": 0, "_": 0,
                                "1": 0, "2": 0, "3": 0,
                                "4": 0, "5": 0, "6": 0,
                                "7": 0, "8": 0, "9": 0,
                                "0": 0}

        self.valid_var_chars_start = {"a": 0, "b": 0, "c": 0,
                                "d": 0, "e": 0, "f": 0,
                                "g": 0, "h": 0, "i": 0,
                                "j": 0, "k": 0, "l": 0,
                                "m": 0, "n": 0, "p": 0,
                                "q": 0, "r": 0, "s": 0,
                                "t": 0, "u": 0, "v": 0,
                                "h": 0, "i": 0, "j": 0,
                                "k": 0, "l": 0, "m": 0,
                                "n": 0, "o": 0, "p": 0,
                                "q": 0, "r": 0, "s": 0,
                                "t": 0, "u": 0, "v": 0,
                                "w": 0, "r": 0, "x": 0,
                                "y": 0, "z": 0, "_": 0}

        self.operations = {}

        self.pos = pos
        self.args = args
        self.data = data

    def char_after_whitespace(self, temp_pos):
        while (self.data[temp_pos]  in self.whitespace):
            temp_pos += 1
        
        return temp_pos, self.data[temp_pos]

    def parse(self):
        found = False
        start = self.pos
        while (self.pos < len(self.data) - 1):
            if (self.data[self.pos] == "}"):
                self.args += "}\n"
                return

            if (self.data[self.pos] in self.whitespace or found):
                pass
            else:
                start = self.pos
                found = True

            if (self.data[start:self.pos] in self.keywords 
                and (ord(self.data[self.pos]) < 65
                or ord(self.data[self.pos]) > 122)):
                return self.keywords[self.data[start:self.pos]]()
            elif (self.data[start:self.pos] in self.variables 
                  and self.data[start:self.pos] not in self.valid_var_chars):

                var_to_declare = self.data[start:self.pos]

                if (self.char_after_whitespace(self.pos)[1] == "="):
                    self.pos = self.char_after_whitespace(self.pos)[0] + 1
                    return self.declare_prex_variable(var_to_declare, self.variables[var_to_declare][0])

                else:
                    print(f"Expected a '=' after {var_to_declare}, causing a failed compilation")
                    exit()

            elif (self.data[start:self.pos] in self.temp_variables 
                  and self.data[start:self.pos] not in self.valid_var_chars):

                var_to_declare = self.data[start:self.pos]

                if (self.char_after_whitespace(self.pos)[1] == "="):
                    self.pos = self.char_after_whitespace(self.pos)[0] + 1
                    return self.declare_prex_variable(var_to_declare, self.temp_variables[var_to_declare][0])
                else:
                    print(f"Expected a '=' after temporary {var_to_declare}, causing a failed compilation")
                    exit()

            self.pos += 1

        return self.args

    def read_after_bool(self):
        var_found = False
        pass
        

    def perform_if(self):
        string = ""
        while (self.data[self.pos] in self.whitespace):
            self.pos += 1

        if (self.data[self.pos] != "("):
            print("Expected a '(' before if statement body")
            exit()
        
        while (self.data[self.pos] != "{"):
            string += self.data[self.pos]
            self.pos += 1
        
        self.args += f"if {string} {{\n"
        self.pos += 1
        self.parse()
        self.pos += 1
        return self.parse()
        # Function can be further refined. Needs to read variable names and determine operations based on that


    def perform_elseif(self):
        pass


    def declare_prex_variable(self, to_declare, var_type):
        string = "" 
        if (var_type == "String"):
            variables = self.read_after_string()
            self.args += f"{to_declare}_len = 0;\n"
            for i in variables:
                if (i[1] == "var"):
                    self.args += f"add_str({to_declare}, {i[0]}, &{to_declare}_len, {i[0]}_len, &{to_declare}_max_length);\n"
                elif (i[1] == "str"):
                    self.args += f"add_str({to_declare}, {i[0]}, &{to_declare}_len, {i[2] - 1}, &{to_declare}_max_length);\n"
            self.pos += 1

            return self.parse()

        elif (var_type == "Int"):
            while (self.data[self.pos] != ";"):
                string += self.data[self.pos]
                self.pos += 1

        elif (var_type == "Float32"):
            string = self.read_after_float32()
            self.pos += 1

        elif (var_type == "Float64"):
            string = self.read_after_float64()
            self.pos += 1

        
        self.args += f"{to_declare} = {string};\n"
        self.pos += 1

        return self.parse()

    def perform_operation(self):
        args = []
        types = []
        op_name = ""
        self.skip_whitespace()
        while (self.data[self.pos] in self.valid_var_chars):
            op_name += self.data[self.pos]
            self.pos += 1

        self.skip_whitespace()
        if (self.data[self.pos] != '('):
            print(f"Error: Missing '(' for function declaration of {op_name}")

        self.pos+=1
        
        found_type = False
        found_var = False
        string = ""
        while (self.data[self.pos] in self.valid_var_chars
               and self.data[self.pos] in self.whitespace):
            if (self.data[self.pos] == self.whitespace):
                if (not found_type):
                    continue
                elif (not found_var):
                    pass
        #Function still yet to be completed
        #Will require changes to how variables are stored within compiler to work.
                



    def return_length(self):
        pass


    def return_string(self):
        string = ""
        curr_variable = ""
        variables = []
        while (self.pos < len(self.data) - 1):
            if  (curr_variable in self.variables):
                variables.append(curr_variable)
                string += self.string_type_conversion[self.variables[curr_variable][0]]
                curr_variable = ""
            elif (curr_variable in self.temp_variables):
                variables.append(self.temp_variables[curr_variable][1])
                string += self.string_type_conversion[self.temp_variables[curr_variable][0]]
                curr_variable = ""


            if (self.data[self.pos] == ";"):
                break

            elif (self.data[self.pos] in self.whitespace):
                curr_variable = ""

            else:
                curr_variable += self.data[self.pos]

            if (self.data[self.pos] == '"'):
                curr_variable = ""
                for self.pos in range(self.pos+1, len(self.data)):
                    if (self.data[self.pos] == '"'):
                        break

                    string += self.data[self.pos]

            self.pos += 1


        self.pos += 1
        return string, variables



    def skip_whitespace(self):
        self.pos += 1
        while (self.data[self.pos] in self.whitespace):
            self.pos += 1


    def perform_loop(self):
        variable_name = ""
        var_type = ""
        step = "1"
        self.skip_whitespace()
        while(self.data[self.pos] not in self.whitespace):
            variable_name += self.data[self.pos]
            self.pos += 1

        self.skip_whitespace()
        temp = ""
        while (self.data[self.pos] not in self.whitespace):
            temp += self.data[self.pos]
            if (temp == "from"):
                self.skip_whitespace()
                start = ""
                while (self.data[self.pos] not in self.whitespace):
                    start += self.data[self.pos]
                    self.pos += 1

                self.skip_whitespace()
                temp = ""
                while (self.data[self.pos] not in self.whitespace):
                    temp += self.data[self.pos]
                    self.pos += 1
                self.skip_whitespace()
                end = ""
                while (self.data[self.pos] not in self.whitespace):
                    end += self.data[self.pos]
                    self.pos += 1
                self.skip_whitespace()
                temp = ""
                while (self.data[self.pos] not in self.whitespace):
                    if (self.data[self.pos] == '{'):
                        self.pos += 1
                        break
                    else:
                        temp += self.data[self.pos]
                        if (temp == "by"):
                            self.skip_whitespace()
                            step = ""
                            while (self.data[self.pos] not in self.whitespace):
                                step += self.data[self.pos]
                                self.pos += 1
                            
                            temp = ""
                            self.skip_whitespace()
                        self.pos += 1
                try: 
                    start_int = int(start)
                    end_int = int(end)
                except ValueError:
                    print("Please supply a valid integer to from command")
                    exit()
                if (start < end):
                    self.args += f"for (int {variable_name} = {start}; {variable_name} < {end}; {variable_name} += {step}) {{\n"
                else: 
                    self.args += f"for (int {variable_name} = {start}; {variable_name} > {end}; {variable_name} += {step}) {{\n"
                self.temp_variables.update({variable_name: ("Int", variable_name)})
                break
            elif (temp == "through"):
                self.skip_whitespace()
                variable_from = ""
                while (self.data[self.pos] != "{"):
                    if (self.data[self.pos] in self.whitespace):
                        self.pos+=1
                        continue

                    variable_from += self.data[self.pos]
                    self.pos += 1

                if (variable_from in self.variables):
                    if (self.variables[variable_from][0] == "String"):
                        self.temp_variables.update({variable_name: ("Char", f"{variable_from}[i]")})
                        self.args += f"for (int i = 0; i < {variable_from}_len; ++i) {{\n"
                        self.pos += 1
                else:
                    print(f"'{variable_from}' is not a declared variable. Please enter a valid variable name")
                    exit()
                break

            self.pos += 1
        
        self.parse()
        del self.temp_variables[variable_name]
        self.pos += 1
        return self.parse()

    def extract_variable_name(self):
        variable_name = ""
        while (self.data[self.pos] not in self.whitespace):
            variable_name += self.data[self.pos]
            self.pos += 1

        while (self.pos < len(self.data) - 1):
            if (self.data[self.pos] in self.whitespace):
                self.pos += 1
                continue

            elif (self.data[self.pos] != "="):
                print("Expected '=' after declaration of new variable, Compilation failed!")
                exit() 
            else:
                break
        self.pos += 1
        return variable_name




    def new_int(self):
        string = ""
        self.skip_whitespace()
        variable_name = self.extract_variable_name()

        while (self.data[self.pos] in self.math_symbols):
            string += self.data[self.pos]
            self.pos += 1

        if (self.data[self.pos] == ";"):
            self.args += f"int {variable_name} = {string};\n"
            self.variables.update({variable_name: ("Int", variable_name)})
            self.pos += 1
        else:
            print(f"Missing a ';' after declaration of {variable_name}")
            exit()

        return self.parse()

    def read_after_string(self):
        variables = []
        curr_variable = ""
        in_quotations = False
        var_found = False
        while (self.pos < len(self.data) - 1):
            if (self.data[self.pos] == '"' and in_quotations == False):
                in_quotations = True
                quote_count = 0

            elif (self.data[self.pos] == '"' and in_quotations == True):
                variables.append((curr_variable + self.data[self.pos], "str", quote_count))
                in_quotations = False
                curr_variable = ""
                quote_count = 0

            if (in_quotations):
                curr_variable += self.data[self.pos]
                quote_count += 1

            else:
                if (self.data[self.pos] in self.valid_var_chars_start):
                    var_found = True

                if (var_found):
                    curr_variable += self.data[self.pos]
                    if (curr_variable in self.variables
                        and self.data[self.pos+1] not in self.valid_var_chars):
                        var_found = False
                        if (self.variables[curr_variable][0] == "String"):
                            variables.append((curr_variable, "var"))
                            curr_variable = ""
                        elif (self.variables[curr_variable][0] == "Int"):
                            variables.append((curr_variable, "int"))
                            curr_variable = ""
                        else:
                            print(f"Error: '{curr_variable}' is of type {self.variables[curr_variable][0]}. Incompatible")  
                            exit()

                    elif (curr_variable not in self.variables
                          and self.data[self.pos+1] not in self.valid_var_chars):
                        print(f"Error: '{curr_variable}' is an undeclared variable. Consider declaring it")
                        exit()

            if (self.data[self.pos] == ';' and in_quotations == False):
                break

            self.pos += 1

        return variables


    def read_after_float32(self):
        string = ""
        var_name = ""
        var_found = False
        valid_float = False

        while (self.data[self.pos] in self.math_symbols or 
               self.data[self.pos] in self.valid_var_chars or 
               self.data[self.pos] == ";"):

            if (self.data[self.pos] in self.valid_var_chars_start and not var_found):
                var_found = True
                var_name += self.data[self.pos]
        
            elif (self.data[self.pos] in self.valid_var_chars and var_found):
                var_name += self.data[self.pos]

            if (self.data[self.pos] not in self.valid_var_chars and var_found):
                if (var_name in self.variables):

                    if (self.variables[var_name][0] == "Float32"):
                        string += var_name
                    elif (self.variables[var_name][0] == "Float64"):
                        string += var_name
                    elif (self.variables[var_name][0] == "Int"):
                        print(f"Warning: '{var_name}' is of type i32. Consider converting '{var_name}' to f32 before operating")
                        string += var_name
                    elif (self.variables[var_name][0] == "Char"):
                        print(f"Error: '{var_name}' is of type char. Consider converting '{var_name}' to f32")
                        exit()
                    elif (self.variables[var_name][0] == "String"):
                        print(f"Error: '{var_name}' is of type str. Consider converting '{var_name}' to f32")
                        exit()

                    var_name = ""
                    var_found = False
                else:
                    print(f"Error: {var_name} is an undeclared variable. Consider declaring it before operation")
                    exit()

            if (self.data[self.pos] == ";"):
                break

            if (self.data[self.pos] in self.float_numerals 
                and self.data[self.pos + 1] not in self.float_numerals
                and valid_float == False):
                string += f"{self.data[self.pos]}.0"
            elif (self.data[self.pos] in self.float_numerals
                  and self.data[self.pos + 1] in self.float_numerals):

                string += self.data[self.pos]

            elif (self.data[self.pos] in self.math_symbols):
                string += self.data[self.pos]


            if (self.data[self.pos] == '.'):
                valid_float = True

            elif (self.data[self.pos] not in self.float_numerals):
                valid_float = False

            self.pos += 1
        
        return string

    def read_after_float64(self):
        string = ""
        var_name = ""
        var_found = False
        valid_float = False

        while (self.data[self.pos] in self.math_symbols or 
               self.data[self.pos] in self.valid_var_chars or 
               self.data[self.pos] == ";"):

            if (self.data[self.pos] in self.valid_var_chars_start and not var_found):
                var_found = True
                var_name += self.data[self.pos]
        
            elif (self.data[self.pos] in self.valid_var_chars and var_found):
                var_name += self.data[self.pos]

            if (self.data[self.pos] not in self.valid_var_chars and var_found):
                if (var_name in self.variables):
                    if (self.variables[var_name][0] == "Float64"):
                        string += var_name
                    elif (self.variables[var_name][0] == "Float32"):
                        print(f"Warning: '{var_name}' is of type f32. Consider converting '{var_name}' to f64 before operating")
                        string += var_name

                    elif (self.variables[var_name][0] == "Int"):
                        print(f"Warning: '{var_name}' is of type i32. Consider converting '{var_name}' to f64 before operating")
                        string += var_name
                    elif (self.variables[var_name][0] == "Char"):
                        print(f"Error: '{var_name}' is of type char. Consider converting '{var_name}' to f64")
                        exit()
                    elif (self.variables[var_name][0] == "String"):
                        print(f"Error: '{var_name}' is of type str. Consider converting '{var_name}' to f64")
                        exit()

                    var_name = ""
                    var_found = False
                else:
                    print(f"Error: {var_name} is an undeclared variable. Consider declaring it before operation")
                    exit()

            if (self.data[self.pos] == ";"):
                break

            if (self.data[self.pos] in self.float_numerals 
                and self.data[self.pos + 1] not in self.float_numerals
                and valid_float == False):
                string += f"{self.data[self.pos]}.0"
            elif (self.data[self.pos] in self.float_numerals
                  and self.data[self.pos + 1] in self.float_numerals):

                string += self.data[self.pos]

            elif (self.data[self.pos] in self.math_symbols):
                string += self.data[self.pos]


            if (self.data[self.pos] == '.'):
                valid_float = True

            elif (self.data[self.pos] not in self.float_numerals):
                valid_float = False

            self.pos += 1
        
        return string
        

    def new_float32(self):
        variable_name = ""
        self.skip_whitespace()
        variable_name = self.extract_variable_name()
        string = self.read_after_float32()

        if (self.data[self.pos] == ";"):
            self.args += f"float {variable_name} = {string};\n"
            self.variables.update({variable_name: ("Float32", variable_name)})
            self.pos += 1
        else:
            print(f"Missing a ';' after declaration of {variable_name}")
            exit()

        return self.parse()


    def new_float64(self):
        variable_name = ""
        self.skip_whitespace()
        variable_name = self.extract_variable_name()

        string = self.read_after_float64()

        if (self.data[self.pos] == ";"):
            self.args += f"double {variable_name} = {string};\n"
            self.variables.update({variable_name: ("Float64", variable_name)})
            self.pos += 1
        else:
            print(f"Missing a ';' after declaration of {variable_name}")
            exit()

        return self.parse()


    def new_string(self):
        variable_name = ""
        total_size = "("
        self.skip_whitespace()
        variable_name = self.extract_variable_name()
        variables = self.read_after_string()
        if (self.data[self.pos] != ';'):
            print(f"Error: Expected a ';' at end of string declaration of {variable_name}")
            exit()

        self.pos += 1

        self.args += f"int {variable_name}_len = 0;\n"
        self.args += f"int {variable_name}_max_length = 10;\n"
        self.args += f"char* {variable_name} = malloc(sizeof(char) * {variable_name}_max_length);\n"
        
        for i in variables:
            if (i[1] == "var"):
                self.args += f"add_str({variable_name}, {i[0]}, &{variable_name}_len, {i[0]}_len, &{variable_name}_max_length);\n"
            elif (i[1] == "str"):
                self.args += f"add_str({variable_name}, {i[0]}, &{variable_name}_len, {i[2] - 1}, &{variable_name}_max_length);\n"
            elif (i[1] == "int"):
                self.args += f"add_int_str({variable_name}, {i[0]}, &{variable_name}_len, &{variable_name}_max_length);\n"

        
        


        #string, variables = self.return_string()
        self.variables.update({variable_name: ("String", variable_name)})

        return self.parse()

    def perform_print(self):
        string, variables = self.return_string()
        self.args += f'printf("{string}"'
        for i in variables:
            self.args += f',{i}'

        self.args += ");\n"

        
        self.pos += 1 
        return self.parse() 

    def perform_println(self):
        string, variables = self.return_string()
        self.args += f'printf("{string}\\n"'
        for i in variables:
            self.args += f',{i}'

        self.args += ");\n"

        
        self.pos += 1 
        return self.parse() 


def open_file(filename):
    fp = open(filename, "r")
    data = fp.read()
    fp.close()
    return data

def run():
    scaffold = """#include "libs/libraries.h"\n int main() { """
    args = ""
    data = open_file(sys.argv[1])
    parser = Parser(data, 0, args)
    args = parser.parse()
    scaffold += args
    scaffold += "}"
    fp = open("test.c", "w")
    fp.write(scaffold)
    fp.close()
    subprocess.Popen("gcc -o test test.c", stdout=subprocess.PIPE, shell = True)

start = time.time()
run()
print(f"Compilation time was {time.time() - start}")

