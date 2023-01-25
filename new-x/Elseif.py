import Errors
import Constants
from PrimitiveErrors import PrimitiveErrors
from BuiltinErrors import BuiltinErrors
from Bool import Bool
from Scope import Scope
from If import If



class Elseif(PrimitiveErrors, BuiltinErrors):
    def __init__(self, valid_variables, valid_types, keywords):
        self.valid_variables = valid_variables
        self.valid_types = valid_types
        self.scope = Scope(valid_variables.copy(), valid_types, keywords)
        self.boolean = Bool(self.valid_variables, self.valid_types)

    def bad_ordering(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Bad ordering of elseif statement")
        Errors.println("if or elseif statement expected before")
        Errors.println("")

    def parse(self, tokenized_text, split_lines, pos, line_count, scope_body):
        if not isinstance(scope_body[-1], If) and not isinstance(scope_body[-1], Elseif):
            self.bad_ordering(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)
        
        try:
            end_idx = tokenized_text.index('{', pos)
            temp_pos, line_count, valid = self.boolean.parse_body(tokenized_text[pos:end_idx] + [';'], 
                                                           split_lines, 0, line_count,
                                                           [])
            if valid:
                self.boolean.linked_list[0].pop()

            pos = end_idx + 1
            return self.scope.parse(tokenized_text, split_lines, pos, line_count)


            

        except ValueError:
            super().expected_curly_brackets(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)


    def return_string(self):
        return f"else if ({self.boolean.return_string()}) {self.scope.return_string()}"
