import Errors
import Constants
import Regex
import unittest
from i32 import i32
from PrimitiveErrors import PrimitiveErrors
from Scope import Scope





class Loop(PrimitiveErrors):
    def __init__(self, valid_variables, builtins):
        self.valid_variables = valid_variables
        self.builtins = builtins
        self.scope = Scope(self.valid_variables.copy(), Constants.PRIMITIVES, Constants.BUILTINS)
        self.body = []
        self.end = None
        self.start = None
        self.by = 1
    
    def expected_curly_brackets(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Expected a '{' before start of operation body")
        Errors.println("") 

 
    def parse_number_loop(self, tokenized_text, split_lines, pos, line_count):
        variable_name = str(tokenized_text[pos])
        new_object = i32(self.valid_variables, Constants.BUILTINS)
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)

        self.start = tokenized_text[pos]
        new_object.linked_list.append(f"int {variable_name} = {self.start};")
        new_object.name = variable_name
        self.loop_variable = new_object
        self.scope.valid_variables.update({variable_name : new_object})
        self.valid_variables.update({variable_name : new_object})

        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)

        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)

        self.end = tokenized_text[pos]
        
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        return self.scope.parse(tokenized_text, split_lines, pos, line_count)

    def parse(self, tokenized_text, split_lines, pos, line_count):
        try:
            idx = tokenized_text.index('{', pos)
            to_match = " ".join(tokenized_text[pos:idx]).replace("\n", "")
            if Regex.number_loop.match(to_match) != None:
                return self.parse_number_loop(tokenized_text, split_lines, pos, line_count)
            else:
                return False


        except ValueError:
            self.expected_curly_brackets(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)

    def return_string(self):
        string = f"for ({self.loop_variable.return_string()}"
        string += str(self.loop_variable.name) + "<" + str(self.end) + ";"
        string += "++" + str(self.loop_variable.name) + ")" 
        string += self.scope.return_string()
        return string





class Test(unittest.TestCase):
    def test_regex_matching(self):
        string = ["i", "from", "1", "to", "10", "{"]
        new_object = Loop({}, {})
        new_object.parse(string, string, 0, 0)
        self.assertEqual(new_object.start, '1', "should be 1")
        self.assertEqual(new_object.end, "10", "Should be 10")

    def test_bad_match(self):
        string = ["i", "fro", "5", "t", "100", "{"]
        new_object = Loop({}, {})
        valid = new_object.parse(string, string, 0, 0)
        self.assertEqual(valid, False, "Valid should return false")

    def test_return_string(self):
        string = ["i", "from", "1", "to", "10", "{", "}"]
        new_object = Loop({}, {})
        new_object.parse(string, string, 0, 0)
        string = "for (int i = 1;i<10;++i){\n}\n"
        self.assertEqual(new_object.return_string(), string, "Should be different")



        




if __name__ == "__main__":
    unittest.main()
