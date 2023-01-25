import Errors
from PrimitiveErrors import PrimitiveErrors
import Constants
import collections

class Bool(PrimitiveErrors):
    def __init__(self, valid_variables, builtins):
        self.valid_variables = valid_variables
        self.builtins = builtins
        self.linked_list = collections.deque()
        self.index = 0
        self.type = "bool"
        self.print_type = "%d"

    def bad_type(self, split_lines, line_count, name, itype):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.printbold(name)
        Errors.println(f" of type \"{itype}\" does not support operation with type bool")
        Errors.println("")

    def find_boolean_symbol(self, tokenized_text, pos):
        while pos < len(tokenized_text):
            if tokenized_text[pos] == '\n':
                pos += 1
            elif tokenized_text[pos] in Constants.BOOLEAN_OPERATORS:
                return pos 
            else:
                pos += 1

        return pos

    def find_logical_symbol(self, tokenized_text, pos):
        while pos < len(tokenized_text):
            if tokenized_text[pos] == '\n':
                pos += 1
            elif tokenized_text[pos] in Constants.LOGICAL_OPERATORS:
                return pos
            elif tokenized_text[pos] == ';':
                return pos
            else:
                pos += 1

        return pos

    def parse_body(self, tokenized_text, split_lines, pos, line_count, body):
        expected_logical = False
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

            elif expected_logical:
                if tokenized_text[pos] not in Constants.LOGICAL_OPERATORS:
                    super().bad_definition(split_lines, line_count)
                    return super().skip_to_end(tokenized_text, pos, line_count)
                else:
                    body.append(tokenized_text[pos])
                    expected_logical = False
                    pos += 1
            
            if tokenized_text[pos] in self.valid_variables and self.valid_variables[tokenized_text[pos]].type == "bool":
                body.append(tokenized_text[pos])
                expected_logical = True
                pos += 1

            else:
                new_object = Constants.PRIMITIVES["i32"](self.valid_variables, self.builtins)
                terminating_pos = self.find_boolean_symbol(tokenized_text, pos)
                if tokenized_text[terminating_pos] not in Constants.BOOLEAN_OPERATORS:
                    super().expected_symbol(split_lines, line_count)
                    return super().skip_to_end(tokenized_text, pos, line_count)

                
                valid = new_object.parse_body(tokenized_text[pos:terminating_pos] + [';'], 
                                              split_lines, 0, line_count, [])[2]
                if valid:
                    body.append(new_object)
                    new_object.linked_list[0].pop()

                else:
                    super().bad_definition(split_lines, line_count)
                    return super().skip_to_end(tokenized_text, pos, line_count)

                expected_logical = True
                body.append(tokenized_text[terminating_pos])
                other_new_object = Constants.PRIMITIVES["i32"](self.valid_variables, self.builtins)
                other_terminating_pos = self.find_logical_symbol(tokenized_text, terminating_pos)

                valid = other_new_object.parse_body(
                        tokenized_text[terminating_pos+1:other_terminating_pos] + [';'],
                        split_lines, 0, line_count, [])[2]
                if valid:
                    body.append(other_new_object)
                    other_new_object.linked_list[0].pop()

                else:
                    super().bad_definition(split_lines, line_count)

                pos = other_terminating_pos

        return pos, line_count, False

    #TODO finish this function to parse boolean body

    
    def parse(self, tokenized_text, split_lines, pos, line_count):
        body = []
        name = tokenized_text[pos]
        if len(self.linked_list) == 0:
            body.append("bool " + name)
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

        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)

        return self.parse_body(tokenized_text, split_lines, pos, line_count, body)


    def return_string(self):
        string = ""
        for i in self.linked_list[self.index]:
            if isinstance(i, str):
                string += i
            else:
                string += i.return_string()

        self.index += 1
        return string
    


if __name__ == "__main__":
    new_object = Bool({}, {})
    string = ["thing", "=", "5", "+", "10", ">", "15", ";"]
    new_object.parse(string, ["thing = 5 + 10 > 15;"], 0, 0)
    print(new_object.return_string())

    

































