import Errors
import Constants
import Regex
import hashlib
from i32 import i32
from GlobalScope import GlobalScope

class Parser:
    def __init__(self, tokenized_text, line_text):
        self.tokenized_args = tokenized_text
        self.line_text = line_text
        self.scope = GlobalScope({}, Constants.PRIMITIVES, Constants.VALID_GLOBAL_KEYWORDS)


    def parse(self):
        self.scope.parse(self.tokenized_args, self.line_text)

    def return_converted_code(self):
        return self.scope.return_string()


   

class Scope:

    def __init__(self, valid_variables, valid_keywords):
        self.valid_variables = valid_variables
        self.primitives = Constants.PRIMITIVES
        self.valid_keywords = valid_keywords


    def return_string(self):
        pass




"""
class Scope:
    
    def __init__(self, valid_variables, valid_keywords, builtins):
        self.valid_variables = valid_variables
        self.valid_keywords = valid_keywords
        self.builtins = builtins
        self.curly_surrounds = True
        self.args_list = []


    def parse(self, tokenized_text, lines, pos=0, line_count=0):
        line_count = 0 
        while (pos < len(tokenized_text)):
            if (tokenized_text[pos].isspace()):
                if (tokenized_text[pos] == '\n'):
                    line_count += 1
                pos += 1
                continue

            elif tokenized_text[pos] == "}":
                return pos+1, line_count
            
            elif (tokenized_text[pos] in self.valid_keywords):
                new_object = self.valid_keywords[tokenized_text[pos]](self.valid_variables.copy(),
                                                                      Constants.VALID_KEYWORDS,
                                                                      Constants.BUILTINS)
                new_pos, line_count = new_object.parse(tokenized_text, lines,
                                                       pos+1, line_count)
                
                self.valid_variables.update({new_object.name : new_object})
                self.args_list.append(new_object)
                pos = new_pos


            elif (tokenized_text[pos] in self.builtins):
                new_object = self.builtins[tokenized_text[pos]](self.valid_variables.copy())
                new_pos, line_count = new_object.parse(tokenized_text, lines,
                                                       pos+1, line_count)

                self.args_list.append(new_object)
                pos = new_pos


            elif (tokenized_text[pos] in self.valid_variables):
                pos += 1

            
            else:
                Errors.printerror(f"Error on line {line_count+1}: ")
                Errors.println(f"{lines[line_count]}")
                Errors.printbold(f"{tokenized_text[pos]}")
                Errors.println(" is an undeclared variable or invalid keyword")
                Errors.println("")
                pos += 1



    def return_string(self):
        string = ""
        if self.curly_surrounds:
            string += '{\n'

        for i in self.args_list:
            string += i.return_string()

        if self.curly_surrounds:
            string += "}\n"
        
        return string


def invalid_name(name, line_text, line_count):
    Errors.line_error(line_text[line_count], line_count)
    Errors.printbold(f"{name} ")
    Errors.println("has unsupported character order for name declaration")
    Errors.println("")

class Operation:
    def __init__(self, valid_variables, valid_keywords, builtins):
        self.scope = Scope(valid_variables, valid_keywords, builtins)
        self.parameters = []
        self.return_type = None
    

    def parameter_error(self, line_text, line_count):
        Errors.line_error(line_text[line_count], line_count)
        Errors.normal_print(f"Improper declaration of parameters for operation ")
        Errors.printboldln(self.name)

    def uneven_parameter_number(self, line_text, line_count):
        Errors.line_error(line_text[line_count], line_count)
        Errors.println("Uneven number of parameters in operation parameter declaration")
        Errors.println("")

    def parse_parameters(self, tokenized_text, line_text, line_count):
        if (tokenized_text[0] != '(' or tokenized_text[len(tokenized_text) - 1] != ')'):
            self.parameter_error(line_text, line_count)
            return False

            
        else:
            if (tokenized_text == "()"):
                self.parameters = []
                return True


            parameter_list = tokenized_text[1:len(tokenized_text) - 1].split(",")
                
            for i in parameter_list:
                if len(i) != 2:
                    self.uneven_parameter_number(line_text, line_count)
                    return False
    
    #TODO Finish this part of the method so it supports function arguments 

    def bad_return_type(self, tokenized_text, line_text, line_count):
        Errors.line_error(line_text[line_count], line_count)
        Errors.normal_print(f"{tokenized_text} is a bad type for return type of operation ")
        Errors.printboldln(f"{self.name}")


    def get_return_type(self, tokenized_text, line_text, line_count):
        if (tokenized_text not in self.scope.valid_keywords):
            self.bad_return_type(tokenized_text, line_text, line_count)
            return False

        self.return_type = tokenized_text

    def expected_curly_brackets(self, line_text, line_count):
        Errors.line_error(line_text[line_count], line_count)
        Errors.println("Expected a '{' before start of operation body")
        Errors.println("") 


    def parse(self, tokenized_text, line_text, pos, line_count):
        name = tokenized_text[pos]
        if (Regex.valid_variable_name.match(name) == None):
            invalid_name(name, line_text, line_count)
            return self.scope.parse(tokenized_text, line_text, tokenized_text.index('\n', pos), line_count)

        self.name = name
        self.scope.valid_variables.update({self.name : self})
        
        
        pos += 1 

        if (not self.parse_parameters(tokenized_text[pos], line_text, line_count)):
            return self.scope.parse(tokenized_text, line_text, tokenized_text.index("\n", pos), line_count)

        pos += 1

        if tokenized_text[pos] == "->":
            if not self.get_return_type(tokenized_text[pos+1], line_text, line_count):
                return self.scope.parse(tokenized_text, line_text, tokenized_text.index("\n", pos), line_count)


        elif tokenized_text[pos] == "{":
            self.return_type = None
            return self.scope.parse(tokenized_text, line_text, pos+1, line_count)

        else:
            self.expected_curly_brackets(line_text, line_count)
            return self.scope.parse(tokenized_text, line_text, pos+1, line_count)

        pos += 1

        if tokenized_text[pos] == "{":
            return self.scope.parse(tokenized_text, line_text, pos+1, line_count)

        else:            
            self.expected_curly_brackets(line_text, line_count)
            return self.scope.parse(tokenized_text, line_text, pos+1, line_count)



    def return_string(self):
        if (self.name != "main"):
            in_code_name = 'a' + hashlib.md5(bytes(self.name, "utf-8")).hexdigest()

        else:
            in_code_name = self.name

        string = ""
        return_type = Constants.TYPE_CONVERSION[self.return_type]
        string += (return_type + " " + str(in_code_name))
        string += "("
        for i in self.parameters:
            string += i.return_string()

        string += ")"
        string += self.scope.return_string()
        return string
        
        
class Println:
    def __init__(self, valid_variables):
        self.valid_variables = valid_variables
        self.body = []
    
    def parse(self, tokenized_text, line_text, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos][0] == '"' and tokenized_text[pos][len(tokenized_text[pos])-1] == '"':
                self.body.append(tokenized_text[pos][1:len(tokenized_text[pos]) - 1])
                pos += 1

            elif (tokenized_text[pos] == ';'):
                return pos+1, line_count

            else:
                pos += 1

        #TODO allow for variables to be entered into print argument
        #TODO make method to determine the type printed 

    def return_string(self):
        string = 'printf("'
        for i in self.body:
            string += i

        string += '\\n");\n'
        return string


class i32:
    def __init__(self, valid_variables, valid_keywords, builtins):
        self.valid_variables = valid_variables
        self.builtins = builtins
        self.body = []

    def tokenize_in_brackets(self, tokenized_text, line_text, pos, line_count):
        #TODO return a list of tokenized math string
        return []


    def expected_symbol(self, tokenized_text, line_text, pos, line_count):
        Errors.line_error(line_text[line_count+1], line_count)
        Errors.println("Expected a symbol after digit, but instead got another digit")



    def parse(self, tokenized_text, line_text, pos, line_count):
        name = tokenized_text[pos]
        if (Regex.valid_variable_name.match(name) == None):
            invalid_name(name, line_text, line_count)
        
        self.name = name
        pos += 1
        symbol_expected = False
        while (pos < len(tokenized_text)):
            if tokenized_text[pos][0] == ';':
                return pos+1, line_count

            elif tokenized_text[pos][0] == '(' and tokenized_text[pos][len(tokenized_text[pos])-1] == ')':
                tokenized_in_brackets = self.tokenize_in_brackets(tokenized_text, line_text, pos, line_count)
                self.parse(tokenized_in_brackets, line_text, 0, line_count)
                #TODO Finish this method. Uses a recursive method to work out text is alright

            elif symbol_expected:
                if (tokenized_text[pos].isdigit()):
                    self.expected_symbol(tokenized_text, line_text, pos, line_count)

            elif tokenized_text[pos].isdigit() and not symbol_expected:
                self.body.append(tokenized_text[pos])
                symbol_expected = True

            pos += 1


    def return_string(self):
        string = f"int {self.name} = "
        for i in self.body:
            string += i

        string += ";\n"
        return string

"""
                
            




























