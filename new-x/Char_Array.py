from PrimitiveErrors import PrimitiveErrors
import Regex
import Errors
import collections

class CharArray(PrimitiveErrors):

    def __init__(self, variables, builtins):
        self.valid_variables = variables
        self.print_conversion = "%s"
        self.builtins = builtins
        self.linked_list = collections.deque()
        self.index = 0
        self.type = "char*"

        

    def error_invalid_token(self, tokenized_text, split_lines, pos, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println(f"Invalid token given for declaration of {self.name}")
        return super().skip_to_end(tokenized_text, pos, line_count)



    def parse_new(self, tokenized_text, split_lines, pos, line_count, body):
        pos, line_count = self.skip_lines(tokenized_text, pos+1, line_count)
        if Regex.new_char_array.match(tokenized_text[pos]) == None:
            return self.error_invalid_token(tokenized_text, split_lines, pos, line_count)
        
        number = tokenized_text[pos].split('[')[1].replace("]", "")
        if number.isdigit():
            self.size = number
            body.append(f"malloc(sizeof(char) * {self.size})")

        pos, line_count = self.skip_lines(tokenized_text, pos+1, line_count)
        if (tokenized_text[pos] == ';'):
            body.append(";\n")
        else:
            super().bad_symbol(split_lines, line_count)
            return self.skip_to_end(tokenized_text, pos, line_count)

        self.linked_list.append(body)

        return pos+1, line_count, True

    def parse_string(self, tokenized_text, split_lines, pos, line_count):
        pass

    def parse(self, tokenized_text, split_lines, pos, line_count):
        body = []
        name = tokenized_text[pos]
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if len(self.linked_list) == 0:
            body.append("char* " + name)
        else:
            body.append(name)

        if Errors.isValidName(name, split_lines, line_count):
            self.name = name
        else:
            self.name = None
            return super().skip_to_end(tokenized_text, pos, line_count)

        sign = tokenized_text[pos]
        if sign != "=":
            super().expected_equals(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)

        elif len(self.linked_list) == 0 and sign != '=':
            super().expected_equals(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)

        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        body.append(sign)
        if tokenized_text[pos] == "new":
            return self.parse_new(tokenized_text, split_lines, pos, line_count, body)
        elif tokenized_text[pos][0] == '"':
            return self.parse_string(tokenized_text, split_lines, pos, line_count)
        else:
            return self.error_invalid_token(tokenized_text, split_lines, pos, line_count)

    
    def return_string(self, no_type=False):
        if no_type and self.index == 0:
            self.linked_list[0][0] = self.linked_list[0][0][6:]

        string = "".join(self.linked_list[self.index])
        self.index += 1
        return string



        
