import Errors

class PrimitiveErrors:
    def expected_equals(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Expected a valid variable assigner when defining variable")
        Errors.println("")
    
    def bad_symbol(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Bad symbol given when defining variable")
        Errors.println("")

    def expected_symbol(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Expected a sign but instead got another digit")
        Errors.println("")

    def bad_definition(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Nothing was defined when defining variable")
        Errors.println("")

    def bad_type(self, split_lines, line_count, type1, type2):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println(f"Type {type1} is incompatible with Type {type2}")
        Errors.println("")



    def skip_to_end(self, tokenized_text, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == ";":
                return pos+1, line_count, False
            elif tokenized_text[pos] == '\n':
                line_count += 1

            pos += 1
            
        return pos, line_count, False

    def skip_lines(self, tokenized_text, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == '\n':
                pos += 1
                line_count += 1
            else:
                return pos, line_count

        return pos, line_count


