import Errors


class Println:
    def __init__(self, valid_variables, valid_types, builtins):
        self.valid_variables = valid_variables
        self.builtins = builtins
        self.body = []

    def skip_to_end(self, tokenized_text, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == ";":
                return pos+1, line_count, False
            elif tokenized_text[pos] == '\n':
                line_count += 1

            pos += 1
            
        return pos, line_count, False


    def multi_line_string_error(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Cannot define string over multiple lines")
        Errors.println("")
        


    def parse_in_quotes(self, tokenized_text, split_lines, pos, line_count):
        quoted_text = tokenized_text[pos]
        if quoted_text[len(quoted_text) - 1] != '"':
            return False, line_count

        for i in quoted_text:
            if i == '\n':
                self.multi_line_string_error(split_lines, line_count)
                line_count += 1
                return False, line_count

        return True, line_count





    
    def parse(self, tokenized_text, split_lines, pos, line_count, scope_body):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == '\n':
                line_count += 1

            if tokenized_text[pos][0] == '"' and tokenized_text[pos][len(tokenized_text[pos])-1] == '"':
                valid, line_count = self.parse_in_quotes(tokenized_text, split_lines, pos, line_count)
                if not valid:
                    return self.skip_to_end(tokenized_text, pos, line_count)

                self.body.append(tokenized_text[pos][1:len(tokenized_text[pos]) - 1])
                pos += 1


            elif tokenized_text[pos] in self.valid_variables:
                self.body.append(self.valid_variables[tokenized_text[pos]])
                pos += 1


            elif (tokenized_text[pos] == ';'):
                return pos+1, line_count, True

            else:
                return pos, line_count, False

        #TODO allow for variables to be entered into print argument
        #TODO make method to determine the type printed 

    def return_string(self):
        string = 'printf("'
        string_args = ""
        for i in self.body:
            if isinstance(i, str):
                string += i
            else:
                string += i.print_type
                string_args += ", " + i.name


        string += '\\n"' + string_args + ');\n'
        return string


