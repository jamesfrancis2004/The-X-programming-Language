import Constants
from Class import Class


class GlobalScope:
    def __init__(self, valid_variables, primitives, keywords):
        self.valid_variables = valid_variables
        self.keywords = keywords
        self.primitives = primitives
        self.body = []

    def parse(self, tokenized_text, split_lines, pos=0, line_count=0):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == '\n':
                line_count += 1
                pos += 1

            elif tokenized_text[pos] == "class":
                new_object = Class(self.valid_variables.copy(),
                                   self.primitives,
                                   self.keywords
                                   )
                pos, line_count, valid = new_object.parse_class(tokenized_text, split_lines, 
                                                                pos + 1, line_count)

                if valid:
                    self.body.append(new_object)
                

            elif tokenized_text[pos] in self.primitives:
                new_object = self.primitives[tokenized_text[pos]](self.valid_variables.copy(),
                                                                  Constants.PRIMITIVE_EXPRESSION_BUILTINS)
                pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                   pos+1, line_count)
                if (valid):
                    self.body.append(new_object)
                    self.valid_variables.update({new_object.name : new_object})


            elif tokenized_text[pos] in self.keywords:
                new_object = self.keywords[tokenized_text[pos]](self.valid_variables.copy(),
                                                                Constants.PRIMITIVES,
                                                                Constants.BUILTINS)

                pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                          pos+1, line_count)

                if valid:
                    self.body.append(new_object)
                    self.valid_variables.update({new_object.name : new_object})

                pass

            else:
                pos += 1


    def return_string(self):
        string = ""
        for i in self.body:
            if isinstance(i, Class):
                string += i.return_struct_string()
            else:
                string += i.return_string()
        
        return string

 
