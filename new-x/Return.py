class Return:

    def __init__(self, object_type):
        self.object_type = object_type

    
    def initiate_class(self, valid_variables, valid_types, builtins):
        self.object_type.valid_variables = valid_variables
        self.object_type.valid_types = valid_types
        self.object_type.builtins = builtins
        return self


    def parse(self, tokenized_text, split_lines, pos, line_count, scope_body):
        pos, line_count, valid = self.object_type.parse_body(tokenized_text, split_lines, pos, line_count, [])

        return pos, line_count, valid
        


    def return_string(self):
        return "return " + self.object_type.return_string()

