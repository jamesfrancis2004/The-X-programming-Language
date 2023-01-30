

class Parsing_Functions:
    def skip_to_curly(self, tokenized_text, pos, line_count):
        while (pos < len(tokenized_text)):
            if tokenized_text[pos] == "{":
                return pos+1, line_count, False
            elif tokenized_text[pos] == '\n':
                line_count += 1

            pos += 1

        return pos, line_count, False


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





