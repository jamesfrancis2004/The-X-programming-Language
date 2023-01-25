import Errors
from PrimitiveErrors import PrimitiveErrors;
from BuiltinErrors import BuiltinErrors
from Scope import Scope
from If import If
from Elseif import Elseif

class Else(PrimitiveErrors, BuiltinErrors):
    def __init__(self, valid_variables, valid_types, keywords):
        self.scope = Scope(valid_variables, valid_types, keywords)
    
    def bad_ordering(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Bad ordering of else if statement")
        Errors.println("if or elseif statement expected before")
        Errors.println("")


    def parse(self, tokenized_text, split_lines, pos, line_count, scope_body):
        if not isinstance(scope_body[-1], If) and not isinstance(scope_body[-1], Elseif):
            self.bad_ordering(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)

        try:
            end_idx = tokenized_text.index('{', pos)



            pos = end_idx + 1
            return self.scope.parse(tokenized_text, split_lines, pos, line_count)


        except ValueError:
            super().expected_curly_brackets(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)


    def return_string(self):
        return f"else {self.scope.return_string()}"

    


