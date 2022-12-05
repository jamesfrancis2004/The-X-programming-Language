import Regex
import Errors
import copy
from PrimitiveErrors import PrimitiveErrors
import Constants
import unittest


class Class(PrimitiveErrors):
    def __init__(self, valid_variables, valid_types, valid_keywords):
        self.valid_variables = valid_variables
        self.valid_types = valid_types
        self.valid_keywords = valid_keywords

        self.has_generics = False
        self.generic_keyword = None
        self.body = []
        self.index = 0

        self.generic_types = []
        self.generic_functions = {}
        self.generic_features = {}
        self.operations = {}
        self.class_variables = {}


    def expected_curly_brackets(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Expected a '{' before start of class body")
        Errors.println("") 

    def __str__(self):
        return self.keyword
    

    def parse_generic_class(self, tokenized_text, split_lines, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == '}':
                return pos+1, line_count, False 

            elif tokenized_text[pos] in self.valid_types or tokenized_text[pos] == self.generic_keyword:
                if tokenized_text[pos] == "operation":
                    # TODO code out unique behaviour for operation 
                    pass
                else:
                    new_object = self.valid_types[tokenized_text[pos]](self.valid_variables,
                                                                       Constants.PRIMITIVE_EXPRESSION_BUILTINS)

                    pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                              pos+1, line_count)

                    if valid:
                        self.class_variables.update({new_object.name : new_object})

                    #TODO Work out this method to deal with other primitive types / types


                #TODO work out this method to deal with members of a class

            else:
                pos += 1

    def parse_normal_class(self, tokenized_text, split_lines, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == '}':
                self.valid_types.update({self.keyword : self.copy})
                return pos+1, line_count, True

            elif tokenized_text[pos] == '\n':
                line_count += 1
                pos += 1

            elif tokenized_text[pos] in self.valid_types or tokenized_text[pos] == self.generic_keyword:
                if tokenized_text[pos] == "operation":
                    pass
                else:
                    new_object = self.valid_types[tokenized_text[pos]](self.valid_variables,
                                                                       Constants.PRIMITIVE_EXPRESSION_BUILTINS)
                    pos, line_count, valid = new_object.parse(tokenized_text, split_lines,
                                                              pos+1, line_count)
                    if valid:
                        self.class_variables.update({new_object.name : new_object})

            else:
                pos += 1

        return pos, line_count, False


    def parse_class(self, tokenized_text, split_lines, pos, line_count):
        name = tokenized_text[pos]
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if tokenized_text[pos] != '{':
            self.expected_curly_brackets(split_lines, line_count)

        if Regex.generic_class_name.match(name):
            self.has_generics = True
            split_text = name.split("[")
            self.keyword = split_text[0].replace("[", "")
            self.type = f"struct {self.keyword}* "
            self.generic_keyword = split_text[1].replace("]", "")
            return self.parse_generic_class(tokenized_text, split_lines, pos+1, line_count)

        elif Errors.isValidName(name, split_lines, line_count):
            self.keyword = name
            self.type = f"struct {self.keyword}* "
            return self.parse_normal_class(tokenized_text, split_lines, pos+1, line_count)
        else:
            self.name = None
            return super().skip_to_end(tokenized_text, pos+1, line_count)


    def parse(self, tokenized_text, split_lines, pos, line_count):
        body = []
        name = tokenized_text[pos]
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if (Errors.isValidName(name, split_lines, line_count)):
            self.name = name

        body.append(f"{self.type} {self.name}")
        sign = tokenized_text[pos]
        if sign != "=":
            super().expected_equals(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)
        
        body.append(sign)
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if tokenized_text[pos] == "new":
            pos += 1
            if tokenized_text[pos] == self.keyword:
                body.append(f"malloc(sizeof(struct {self.keyword}))")
            else:
                super().bad_symbol(tokenized_text, line_count)
                super().skip_to_end(tokenized_text, pos, line_count)
        else:
            super().bad_symbol(tokenized_text, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)
            
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)

        if tokenized_text[pos] != ';':
            super().bad_symbol(tokenized_text, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)
        body.append(';\n')

        if len(self.body) == 0:
            for i in self.class_variables.values():
                string = i.return_string(no_type = True)
                string_split = string.splitlines()
                for i in string_split:
                    body.append(f"{self.name}->" + i + "\n")

        self.body.append(body)

        return pos+1, line_count, True

    def parse_inline(self, tokenized_text, split_lines, pos, line_count, string=""):
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if  tokenized_text[pos] == '.':
            pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
            if tokenized_text[pos] in self.class_variables:
                string += f"{self.name}->"
                return self.class_variables[tokenized_text[pos]].parse_inline(tokenized_text,
                                                                       split_lines,
                                                                       pos,
                                                                       line_count,
                                                                       string)
            else:
                super().bad_symbol(split_lines, line_count)
                return string, pos+1, line_count, None
        
        else:
            string += f"{self.name}"
            return string, pos+1, line_count, self




    def return_string(self, no_type=False):
        if no_type and self.index == 0:
            self.body[0][0] =self.body[0][0].replace(f"{self.type} ", "")

        string = "".join(self.body[self.index])
        self.index += 1
        return string

    def return_struct_string(self):
        string = f"struct {self.keyword} {{\n"
        for i in self.class_variables.values():
            string += f"{i.type} {i.name};\n" 

        string += "};\n"

        return string

    def copy(self, *args):
        new_object = copy.deepcopy(self)

        return new_object

    # TODO Improve this method so it is less jank

        








class Tests(unittest.TestCase):
    def test_generic_name(self):
        str_text = ["vec[T]", "{", "}"]
        new_object = Class({}, {}, {})
        new_object.parse_class(str_text, str_text, 0, 0)
        self.assertEqual(new_object.name, "vec", f"should be vec but is {new_object.name}")
        self.assertEqual(new_object.generic_keyword, "T", "should be T")
        self.assertEqual(new_object.has_generics, True, "New object should have generics")

    def test_normal_name(self):
        str_text = ["vec", "{"]
        new_object = Class({}, {}, {})
        new_object.parse_class(str_text, str_text, 0, 0)
        self.assertEqual(new_object.name, "vec", f"should be vec but is {new_object.name}")
        self.assertEqual(new_object.generic_keyword, None, "Should be none")
        self.assertEqual(new_object.has_generics, False, "Object shouldn't have generics")

    def test_bad_name(self):
        str_text = ["vec[]", "{"]
        new_object = Class({}, {}, {})
        new_object.parse_class(str_text, str_text, 0, 0)
        self.assertEqual(new_object.name, None, f"Should have errored and no name")


    def test_generic_class_variable(self):
        str_text = ["vec[T]", "{", "i32", "max_length", "=", "10", ";", "}"]
        new_object = Class({}, Constants.PRIMITIVES, {})
        new_object.parse_class(str_text, str_text, 0, 0)
        self.assertEqual(len(new_object.class_variables), 1, f"Should be one variable")
        
    def test_normal_class_variable(self):
        str_text = ["vec", "{", "i32", "max_length", "=", "10", ";", "}"]
        new_object = Class({}, Constants.PRIMITIVES, {})
        new_object.parse_class(str_text, str_text, 0, 0)
        self.assertEqual(len(new_object.class_variables), 1, f"Should be one variable")


    def test_class_var_return(self):
        str_text = ["vec", "{", "i32", "max_length", "=", "10", ";", "}"]
        new_object = Class({}, Constants.PRIMITIVES, {})
        new_object.parse_class(str_text, str_text, 0, 0)
        for i in new_object.class_variables.values():
            self.assertEqual(i.return_struct_string(), "int max_length;\n", "Should be int max_length")
            self.assertEqual(i.return_string(), "max_length=10;\n", "should be max_length=10;")

    def test_class_return(self):
        str_text = ["vec", "{", "i32", "max_length", "=", "10", ";", "}"]
        should_return = "struct vec {\nint max_length;\n};\n"
        new_object = Class({}, Constants.PRIMITIVES, {})
        new_object.parse_class(str_text, str_text, 0, 0)
        self.assertEqual(new_object.return_struct_string(), should_return, "should return correct struct string")


     

if __name__ == "__main__":
    unittest.main()











