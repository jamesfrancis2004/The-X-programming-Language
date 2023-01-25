from PrimitiveErrors import PrimitiveErrors
import Errors


class Inline_Class(PrimitiveErrors):
    def __init__(self, keyword, itype, class_variables):
        self.keyword = keyword
        self.type = itype
        self.valid_variables = {}
        self.valid_types = {}
        self.linked_list = []
        self.class_variables = class_variables
        self.index = 0
    
    def remove_identifier(self):
        self.linked_list[0].pop(0)

    def initiate_class(self, valid_variables, valid_types):
        new_class = Inline_Class(self.keyword, self.type, self.class_variables)
        new_class.valid_variables = valid_variables
        new_class.valid_types = valid_types

        return new_class

    def parse_inline(self, tokenized_text, split_lines, pos, line_count, string=""):
        body = []
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if  tokenized_text[pos] == '.':
            pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
            if tokenized_text[pos] in self.class_variables:
                body.append(f"{self.name}->")
                body.append(self.class_variables[tokenized_text[pos]])
                self.linked_list.append(body)
                return self.class_variables[tokenized_text[pos]].parse_inline(tokenized_text,
                                                                       split_lines,
                                                                       pos,
                                                                       line_count,
                                                                       string)
            else:
                super().bad_symbol(split_lines, line_count)
                return pos+1, line_count, None
        
        else:
            body.append(f"{self.name}")
            self.linked_list.append(body)
            return pos+1, line_count, self
    
    def parse_body(self, tokenized_text, split_lines, pos, line_count, body):
        if tokenized_text[pos] == "new":
            pos += 1
            if tokenized_text[pos] == self.keyword:
                body.append(f"create_{self.keyword}()")
            else:
                super().bad_symbol(tokenized_text, line_count)
                return super().skip_to_end(tokenized_text, pos, line_count)

        elif tokenized_text[pos] in self.valid_variables:
            if self.valid_variables[tokenized_text[pos]].type == self.type:
                body.append(tokenized_text[pos])
            else:
                super().bad_type(split_lines, line_count,
                                 self.valid_variables[tokenized_text[pos]].keyword,
                                 self.keyword)
                return super().skip_to_end(tokenized_text, pos, line_count)
                
        else:
            super().bad_symbol(tokenized_text, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)
            
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)

        if tokenized_text[pos] != ';':
            super().bad_symbol(tokenized_text, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)
        body.append(';\n')
        self.linked_list.append(body)

        return pos+1, line_count, True

    def reparse(self, tokenized_text, split_lines, pos, line_count, valid_variables):
        body = []
        body.append(tokenized_text[pos])
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if tokenized_text[pos] == '.':
            pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
            if tokenized_text[pos] in self.class_variables:
                body.append("->")
                temp_object = self.class_variables[tokenized_text[pos]]
                pos, line_count, valid = temp_object.reparse(tokenized_text,
                                         split_lines,
                                         pos,
                                         line_count,
                                         self.valid_variables)
                if valid:
                    body.append(temp_object)
                else:
                    return super().skip_to_end(tokenized_text, pos, line_count)
            else:
                super().bad_symbol(split_lines, line_count)
                return super().skip_to_end(tokenized_text, pos, line_count)

        else:
            super().bad_symbol(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)

        self.linked_list.append(body)
        return pos+1, line_count, True
        




    def parse(self, tokenized_text, split_lines, pos, line_count):
        body = []
        name = tokenized_text[pos]
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        if (Errors.isValidName(name, split_lines, line_count)):
            self.name = name
        
        body.append(self.type)
        body.append(self.name)
        sign = tokenized_text[pos]
        if sign != "=":
            super().expected_equals(split_lines, line_count)
            return super().skip_to_end(tokenized_text, pos, line_count)
        
        body.append(sign)
        pos, line_count = super().skip_lines(tokenized_text, pos+1, line_count)
        return self.parse_body(tokenized_text, split_lines, pos, line_count, body)




    def return_string(self):
        string = ""
        for i in self.linked_list[self.index]:
            if isinstance(i, str):
                string += i
            else:
                string += i.return_string()

        self.index += 1

        return string




