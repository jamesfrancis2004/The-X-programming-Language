import Tokenizer
import Errors
import Constants
from Scope import Scope
from Return import Return
from PrimitiveErrors import PrimitiveErrors
from Parsing_Functions import Parsing_Functions



class Inline_Operation(PrimitiveErrors, Parsing_Functions):
    def __init__(self, name, valid_variables, valid_types, return_type, parameters):
        self.name = name
        self.valid_variables = valid_variables
        self.valid_types = valid_types
        self.return_type = return_type
        self.parameters = parameters
        self.linked_list = []
        self.index = 0

    def parameter_error(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.normal_print(f"Improper declaration of parameters for operation ") 
        Errors.printboldln(self.name)


    def initiate_class(self, valid_variables, valid_types):
        self.valid_variables = valid_variables
        self.valid_types = valid_types
        return self

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
                    if idx != len(self.parameters) - 1:
                        param_list_argument.linked_list[-1].pop()
                        param_list_argument.linked_list[-1].append(",")
                        body.append(param_list_argument)
                    else:
                        param_list_argument.linked_list[-1].pop()
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
            return super().skip_to_end(tokenized_text, pos, line_count)

        self.linked_list.append(body)
        return pos+1, line_count, True


    def parse_inline(self, tokenized_text, split_lines, pos, line_count, valid_variables):
        pos, line_count, valid = self.reparse(tokenized_text, split_lines, pos, line_count, valid_variables)
        if valid:
            return pos, line_count, self.valid_types[self.return_type]({},{})
        else:
            return pos, line_count, None
    

    def return_string(self):
        string = ""
        for i in self.linked_list[self.index]:
            if isinstance(i, str):
                string += i
            else:
                string += i.return_string()

        self.index += 1

        return string



