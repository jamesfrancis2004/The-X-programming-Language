import Errors
import Constants
from Scope import Scope


class Operation:
    def __init__(self, valid_variables, primitives, builtins):
        self.scope = Scope(valid_variables, primitives, builtins)
        self.parameters = []
        self.return_type = None
        self.returned_function = False
        self.string_return_list = []
        self.index = 0
    

    def parameter_error(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.normal_print(f"Improper declaration of parameters for operation ")
        Errors.printboldln(self.name)

    def uneven_parameter_number(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Uneven number of parameters in operation parameter declaration")
        Errors.println("")

    def parse_parameters(self, tokenized_text, split_lines, line_count):
        if (tokenized_text[0] != '(' or tokenized_text[len(tokenized_text) - 1] != ')'):
            self.parameter_error(split_lines, line_count)
            return False
            
        else:
            if (tokenized_text == "()"):
                self.parameters = []
                return True


            parameter_list = tokenized_text[1:len(tokenized_text) - 1].split(",")
                
            for i in parameter_list:
                if len(i) != 2:
                    self.uneven_parameter_number(split_lines, line_count)
                    return False
    
    #TODO Finish this part of the method so it supports function arguments 

    def reparse_parameters(self, tokenized_text, split_lines, line_count):
        if len(self.parameters) == 0 and tokenized_text == "()":
            return True

    def bad_return_type(self, tokenized_text, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.normal_print(f"{tokenized_text} is a bad type for return type of operation ")
        Errors.printboldln(f"{self.name}")

    def get_return_type(self, tokenized_text, split_lines, line_count):
        if (tokenized_text not in self.scope.primitives):
            self.bad_return_type(tokenized_text, split_lines, line_count)
            return False

        self.return_type = tokenized_text

    def expected_curly_brackets(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Expected a '{' before start of operation body")
        Errors.println("") 

    def skip_to_end(self, tokenized_text, split_lines, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == "{":
                return self.scope.parse(tokenized_text, split_lines, pos+1, line_count)
            elif tokenized_text[pos] == '\n':
                line_count += 1

            pos += 1

        return pos, line_count, False


    def parse(self, tokenized_text, split_lines, pos, line_count):
        name = tokenized_text[pos]
        if not Errors.isValidName(name, split_lines, line_count):
            return self.skip_to_end(tokenized_text, split_lines, pos, line_count)

        self.name = name
        self.scope.valid_variables.update({self.name : self})
        pos += 1 

        if (not self.parse_parameters(tokenized_text[pos], split_lines, line_count)):
            return self.skip_to_end(tokenized_text, split_lines, pos, line_count)

        pos += 1

        if tokenized_text[pos] == "->":
            if not self.get_return_type(tokenized_text[pos+1], split_lines, line_count):
                return self.skip_to_end(tokenized_text, split_lines, pos, line_count)


        elif tokenized_text[pos] == "{":
            self.return_type = None
            return self.scope.parse(tokenized_text, split_lines, pos+1, line_count)

        else:
            self.expected_curly_brackets(split_lines, line_count)
            return self.scope.parse(tokenized_text, split_lines, pos+1, line_count)

        pos += 1

        if tokenized_text[pos] == "{":
            return self.scope.parse(tokenized_text, split_lines, pos+1, line_count)

        else:            
            self.expected_curly_brackets(split_lines, line_count)
            return self.scope.parse(tokenized_text, split_lines, pos+1, line_count)

    def reparse(self, tokenized_text, split_lines, pos, line_count):
        body = []
        body.append(f"{self.name}")
        pos += 1
        if not self.reparse_parameters(tokenized_text[pos], split_lines, line_count):
            return self.skip_to_end(tokenized_text, split_lines, pos, line_count)
        
        body.append(tokenized_text[pos])
        pos += 1
        self.string_return_list.append(body)
        if tokenized_text[pos] == ";":
            body.append(";\n")
            return pos+1, line_count, True
        else:
            return pos, line_count, True



    def return_string(self):
        if self.returned_function == False:
            self.returned_function = True
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
        else:
            string = "".join(self.string_return_list[self.index])
            self.index += 1
            return string
     
