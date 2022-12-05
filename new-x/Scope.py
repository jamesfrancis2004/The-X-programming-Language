import Constants

class Scope:
    def __init__(self, valid_variables, primitives, builtins):
        self.valid_variables = valid_variables
        self.primitives = primitives
        self.builtins = builtins
        self.body = []

    def parse(self, tokenized_text, split_lines, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == '\n':
                line_count += 1
                pos += 1

            elif tokenized_text[pos] == "}":
                return pos+1, line_count, True

            elif tokenized_text[pos] in self.primitives:
                new_object = self.primitives[tokenized_text[pos]](self.valid_variables,
                                                                  Constants.PRIMITIVE_EXPRESSION_BUILTINS)
                pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                   pos+1, line_count)
                if (valid):
                    self.body.append(new_object)
                    self.valid_variables.update({new_object.name : new_object})

            elif tokenized_text[pos] in self.builtins:
                new_object = self.builtins[tokenized_text[pos]](self.valid_variables,
                                                                Constants.PRIMITIVE_EXPRESSION_BUILTINS)

                pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                          pos+1, line_count)
                if valid:
                    self.body.append(new_object)

            elif tokenized_text[pos] in self.valid_variables:
                defined_variable = self.valid_variables[tokenized_text[pos]]
                pos, line_count, valid = defined_variable.reparse(tokenized_text, split_lines,
                                                                  pos, line_count)
                if valid: 
                    self.body.append(defined_variable)



            else:
                pos += 1

        return pos+1, line_count, False

    def return_string(self):
        string = "{\n"
        for i in self.body:
            string += i.return_string()

        return string + "}\n"
