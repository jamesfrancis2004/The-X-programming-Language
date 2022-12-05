import Errors
from PrimitiveErrors import PrimitiveErrors
import Constants
import collections



class i32(PrimitiveErrors):
    def __init__(self, valid_variables, builtins):
        self.valid_variables = valid_variables
        self.builtins = builtins 
        self.linked_list = collections.deque()
        self.index = 0
        self.type = "int"
        self.print_type = "%d"

    def bad_type(self, split_lines, line_count, name, itype):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.printbold(name)
        Errors.println(f" of type \"{itype}\" does not support operation with type i32")
        Errors.println("")

    def parse_inline(self, tokenized_text, split_lines, pos, line_count, string=""):
        string += tokenized_text[pos]
        return string, pos+1, line_count, self

    def parse_body(self, tokenized_text, split_lines, pos, line_count, body):
        allowed_before_digit = set(["+", "-"])
        expect_symbol = False
        while pos < len(tokenized_text):
            if tokenized_text[pos] == '\n':
                line_count += 1
                pos += 1

            elif tokenized_text[pos] == ';':
                if len(body) == 0:
                    super().bad_definition(split_lines, line_count)
                    self.name = None
                else:
                    body.append(";\n")
                    self.linked_list.append(body)
                
                return pos+1, line_count, True

            if expect_symbol:
                if tokenized_text[pos] in Constants.SYMBOLS:
                    body.append(tokenized_text[pos])
                    expect_symbol = False
                    pos += 1

                else:
                    super().expected_symbol(split_lines, line_count)
                    return super().skip_to_end(tokenized_text, pos, line_count)

            elif not expect_symbol:
                if tokenized_text[pos] in allowed_before_digit:
                    body.append(tokenized_text[pos])
                    pos += 1

                elif tokenized_text[pos].isdigit():
                    body.append(tokenized_text[pos])
                    expect_symbol = True
                    pos += 1

                elif tokenized_text[pos] in self.valid_variables:
                    string, pos, line_count, variable = self.valid_variables[tokenized_text[pos]].parse_inline(tokenized_text,split_lines,
                                                                                                                pos,
                                                                                                                line_count)

                    if not isinstance(variable, i32):
                        self.bad_type(split_lines, line_count, string, str(variable))
                        return super().skip_to_end(tokenized_text, pos, line_count)

                    expect_symbol = True
                    body.append(string)

                else:
                    super().bad_symbol(split_lines, line_count)
                    return super().skip_to_end(tokenized_text, pos, line_count)

        return pos, line_count, True 
                    
    def parse(self, tokenized_text, split_lines, pos, line_count):
        body = []
        name = tokenized_text[pos]
        if len(self.linked_list) == 0:
            body.append("int " + name)
        else:
            body.append(name)

        if Errors.isValidName(name, split_lines, line_count):
            self.name = name
        else:
            self.name = None
            return super().skip_to_end(tokenized_text, pos, line_count)

        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if len(self.linked_list) == 0:
            if tokenized_text[pos] == '=':
                body.append(tokenized_text[pos])
            else:
                super().bad_definition(split_lines, line_count)
                return super().skip_to_end(tokenized_text, pos, line_count)
        else:
            if tokenized_text[pos] in Constants.VALID_ASSIGNMENT_OPERATORS:
                body.append(tokenized_text[pos])
            else:
                super().bad_definition(split_lines, line_count)
                return super().skip_to_end(tokenized_text, pos, line_count)

        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)

        return self.parse_body(tokenized_text, split_lines, pos, line_count, body)

    def reparse(self, tokenized_text, split_lines, pos, line_count):
        return self.parse(tokenized_text, split_lines, pos, line_count)


    def return_string(self, no_type=False):
        if no_type and self.index == 0:
            self.linked_list[0][0] = self.linked_list[0][0][4:]
        
        string = "".join(self.linked_list[self.index])
        self.index += 1
        return string






        
    








