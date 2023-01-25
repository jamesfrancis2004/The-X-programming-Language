import Errors 
import Constants
from PrimitiveErrors import PrimitiveErrors
from BuiltinErrors import BuiltinErrors
from Bool import Bool
from Scope import Scope


class If(PrimitiveErrors, BuiltinErrors):
    def __init__(self, valid_variables, valid_types, keywords):
        self.valid_variables = valid_variables
        self.valid_types = valid_types
        self.keywords = keywords
        self.scope = Scope(valid_variables, valid_types, keywords)
        self.boolean = Bool(self.valid_variables, keywords)


    def parse(self, tokenized_text, split_lines, pos, line_count, scope_body):
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
        return f"if ({self.boolean.return_string()}) {self.scope.return_string()}"
