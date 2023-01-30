import Constants

class Scope:
    def __init__(self, valid_variables, valid_types, keywords):
        self.valid_variables = valid_variables
        self.valid_types = valid_types
        self.keywords = keywords
        self.body = []

    def parse(self, tokenized_text, split_lines, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == '\n':
                line_count += 1
                pos += 1

            elif tokenized_text[pos] == "}":
                return pos+1, line_count, True
                

            elif tokenized_text[pos] in self.valid_types:
                new_object = self.valid_types[tokenized_text[pos]](self.valid_variables,
                                                                  self.valid_types)

                pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                   pos+1, line_count)
                if (valid):
                    self.body.append(new_object)
                    self.valid_variables.update({new_object.name : new_object})

            elif tokenized_text[pos] in self.keywords:
                new_object = self.keywords[tokenized_text[pos]](self.valid_variables,
                                                                self.valid_types,
                                                                self.keywords)

                pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                          pos+1, line_count, self.body)
                if valid:
                    self.body.append(new_object)

            elif tokenized_text[pos] in self.valid_variables:
                defined_variable = self.valid_variables[tokenized_text[pos]]
                pos, line_count, valid = defined_variable.reparse(tokenized_text, split_lines,
                                                                  pos, line_count, self.valid_variables)
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
