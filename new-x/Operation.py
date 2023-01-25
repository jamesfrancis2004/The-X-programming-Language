import Tokenizer
import Errors
import unittest
import Constants
from Scope import Scope
from Return import Return
from PrimitiveErrors import PrimitiveErrors


class Operation(PrimitiveErrors):
    def __init__(self, valid_variables, valid_types, keywords):
        self.scope = Scope(valid_variables, valid_types, keywords)
        self.parameters = []
        self.return_type = None
        self.type = "void"
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

    def non_existent_parameter(self, variable_name, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.normal_print(f"{variable_name} does not match type in parameter or does not exist in scope")

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
                parameter = i.split()
                if len(parameter) != 2:
                    self.uneven_parameter_number(split_lines, line_count)
                    return False

                elif parameter[0] not in self.scope.valid_types:
                    self.parameter_error(split_lines, line_count)
                    return False

                elif not Errors.isValidName(parameter[1], split_lines, line_count):
                    return False

                else:
                    new_object = self.scope.valid_types[parameter[0]](self.scope.valid_variables,
                                                             Constants.PRIMITIVE_EXPRESSION_BUILTINS)
                    new_object.name = parameter[1]
                    new_object.linked_list.append([f"{new_object.type} {new_object.name}"])
                    self.parameters.append(new_object)
                    self.scope.valid_variables.update({new_object.name : new_object})
            return True

        # Checks a function for its parameter list
        # Checks all types are valid 
        # Adds all parameters to scope variable list


    def bad_return_type(self, tokenized_text, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.normal_print(f"{tokenized_text} is a bad type for return type of operation ")
        Errors.printboldln(f"{self.name}")

    def get_return_type(self, return_type, split_lines, line_count):
        if (return_type not in self.scope.valid_types):
            self.bad_return_type(return_type, split_lines, line_count)
            return False
            # Check whether a valid variable type is returned from function

        self.return_type = return_type
        return_object = self.scope.valid_types[return_type]({}, {})
        self.type = return_object.type
        return_object = Return(return_object)
        self.scope.keywords.update({"return": return_object.initiate_class})

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
            pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
            if not self.get_return_type(tokenized_text[pos], split_lines, line_count):
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


    def reparse_parameters(self, tokenized_text, split_lines, line_count, valid_variables, body):
        if len(self.parameters) == 0 and tokenized_text == "()":
            body.append("()")
            return True

        elif len(self.parameters) != 0 and tokenized_text != "()":
            body.append("(")
            tokenizer = Tokenizer.Tokenizer()
            parameter_list = tokenized_text[1:len(tokenized_text) - 1].split(",")
            if len(parameter_list) != len(self.parameters):
                self.parameter_error(split_lines, line_count)

            idx = 0
            for new_argument, param_list_argument in zip(parameter_list, self.parameters):
                tokenizer.tokenize_text(new_argument)
                tokenizer.tokenized_text.append(";")
                param_list_argument.valid_variables = valid_variables
                pos, line_count, valid = param_list_argument.parse_body(tokenizer.tokenized_text,
                                                                        split_lines,
                                                                        0,
                                                                        line_count,
                                                                        [])

                if valid: 
                    if idx != len(parameter_list) - 1:
                        param_list_argument.linked_list[len(param_list_argument.linked_list) - 1].pop()
                        param_list_argument.linked_list[len(param_list_argument.linked_list) - 1].append(",")
                        body.append(param_list_argument)
                    else:
                        param_list_argument.linked_list[len(param_list_argument.linked_list) - 1].pop()
                        body.append(param_list_argument)

                else:
                    self.parameter_error(split_lines, line_count)
                    return False

                idx += 1
            body.append(")")

            return True

        else:
            self.parameter_error(split_lines, line_count)
            return False

     
    def reparse(self, tokenized_text, split_lines, pos, line_count, valid_variables):
        body = []
        body.append(f"{self.name}")
        pos += 1
        if not self.reparse_parameters(tokenized_text[pos], split_lines, line_count, valid_variables, body):
            return self.skip_to_end(tokenized_text, split_lines, pos, line_count)

         
        self.string_return_list.append(body + [';\n'])
        return pos+1, line_count, True

    def parse_inline(self, tokenized_text, split_lines, pos, line_count, valid_variables):
        pos, line_count, valid = self.reparse(tokenized_text, split_lines, pos, line_count, valid_variables)
        if valid:
            return pos, line_count, self.scope.valid_types[self.return_type]({},{})
        else:
            return pos, line_count, None

    def return_string(self):
        string = ""
        if self.returned_function == False:
            self.returned_function = True
            in_code_name = self.name
            string = ""
            string += (self.type + " " + str(in_code_name))
            string += "("
            for idx, i in enumerate(self.parameters):
                if idx == 0:
                    string += i.return_string()
                else:
                    string += f", {i.return_string()}"

            string += ")"
            string += self.scope.return_string()
        else:
            string = ""
            for i in self.string_return_list[self.index]:
                if isinstance(i, str):
                    string += i
                else:
                    string += i.return_string()

            self.index += 1

        return string
    
class Test(unittest.TestCase):
    def test_name(self):
        variable_name = ["printhello", "()", "{"]
        new_object = Operation({}, {}, {})
        new_object.parse(variable_name, variable_name, 0, 0)
        self.assertEqual(new_object.name, "printhello")
        self.assertEqual(new_object.return_type, None)

    def test_return_function(self):
        variable_name = ["printhello", "()", "->", "i32", "{"]
        new_object = Operation({}, Constants.PRIMITIVES, {})
        new_object.parse(variable_name, variable_name, 0, 0)
        self.assertEqual(new_object.name, "printhello")
        self.assertEqual(new_object.return_type, "i32")

    def test_parameter(self):
        variable_name = ["printhello", "(i32 number)", "{"]
        new_object = Operation({}, Constants.PRIMITIVES, {})
        new_object.parse(variable_name, variable_name, 0, 0)
        self.assertEqual(new_object.name, "printhello")
        self.assertEqual(len(new_object.parameters), 1)
        self.assertEqual(new_object.parameters[0].name, "number")

    def test_multiple_parameters(self):
        variable_name = ["printhello", "(i32 number, i32 other_number)", "{"]
        new_object = Operation({}, Constants.PRIMITIVES, {})
        new_object.parse(variable_name, variable_name, 0, 0)
        self.assertEqual(len(new_object.parameters), 2)
        self.assertEqual(new_object.parameters[0].name, "number")
        self.assertEqual(new_object.parameters[1].name, "other_number")
        





if __name__ == "__main__":
    unittest.main()
