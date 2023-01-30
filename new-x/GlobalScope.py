import Constants
from i32 import i32
from Bool import Bool
from Char_Array import CharArray
from Class import Class


class GlobalScope:
    def __init__(self, valid_variables, primitives, keywords):
        self.valid_variables = valid_variables
        self.valid_types = {"i32": i32,
                            "bool": Bool,
                            "f32": None,
                            "f64": None,
                            "char[]": CharArray}


        self.keywords = keywords
        self.primitives = primitives
        self.body = []

    def parse(self, tokenized_text, split_lines, pos=0, line_count=0):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == '\n':
                line_count += 1
                pos += 1


            elif tokenized_text[pos] in self.valid_types:
                new_object = self.valid_types[tokenized_text[pos]](self.valid_variables.copy(),
                                                                  self.valid_types)
                pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                   pos+1, line_count)
                if (valid):
                    self.body.append(new_object)
                    self.valid_variables.update({new_object.name : new_object})


            elif tokenized_text[pos] in self.keywords:
                new_object = self.keywords[tokenized_text[pos]](self.valid_variables,
                                                                self.valid_types,
                                                                Constants.BUILTINS)

                pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                          pos+1, line_count)

                if valid:
                    self.body.append(new_object)



            else:
                pos += 1


    def return_string(self):
        string = ""
        for i in self.body:
            string += i.return_string()
        
        return string

 
