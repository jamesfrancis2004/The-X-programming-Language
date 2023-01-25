import Errors
import Constants

class Tokenizer:
    def __init__(self):
        self.tokenized_text = []
        self.brackets = {"{": "}", 
                         "(": ")"}
        self.line_count = 0


    def line_error(self, text, pos):
            if self.line_count == 0:
                start_line = 0
            else:
                try:
                    start_line = pos - text[pos:0:-1].index('\n') + 1
                except ValueError:
                    start_line = 0

            end_line = text.index('\n', pos)

            Errors.printerror(f"Error on line {self.line_count+1}: ")
            Errors.println(f"{text[start_line:end_line]}")

            return start_line, end_line

    
    def find_bracket_termination(self, text, pos):
        close_count = 1

        while (pos < len(text)):
            if text[pos] == '(':
                close_count += 1

            elif text[pos] == ')':
                close_count -= 1

            elif text[pos] == '"':
                new_pos = self.tokenize_quotes(text, pos)
                if (text[new_pos] == '\n'):
                    pos += 1

                else:
                    pos = new_pos

                continue
            
            if close_count == 0:
                return pos + 1
            
            pos += 1

        return -1 


    def tokenize_brackets(self, text, pos):
        end_pos = self.find_bracket_termination(text, pos+1)
        if (end_pos == -1):
            start_line, end_line =  self.line_error(text, pos)
            Errors.println("^".rjust(pos - (start_line-1) + 16 + len(str(self.line_count))) + " Unterminated parentheses")
            Errors.println("")
            return end_line

            
        else:
            self.tokenized_text.append(text[pos:end_pos])
            return end_pos



    def find_quote_termination(self, text, pos):
        for idx, i in enumerate(text[pos:len(text)]):
            if (i == '"'):
                return idx + pos + 1
        
        return -1

    def tokenize_quotes(self, text, pos):
        end_pos = self.find_quote_termination(text, pos+1)
        if (end_pos == -1):
            start_line, end_line = self.line_error(text, pos)
            Errors.println("^".rjust(pos - (start_line-1) + 16 + len(str(self.line_count))) + " Unterminated quotes")
            Errors.println("")
            return end_line
        else:
            self.tokenized_text.append(text[pos:end_pos])
            return end_pos


    def tokenize_symbol(self, text, pos):
        curr_text = []
        for idx, i in enumerate(text[pos:len(text)]):
            if i in Constants.SYMBOLS:
                curr_text.append(i)
            else:
                return "".join(curr_text), idx+pos

        return "".join(curr_text), len(text)



    def tokenize_text(self, text):
        self.tokenized_text = []
        curr_text = []
        pos = 0
        while (pos < len(text)):
            if (text[pos].isspace()):
                if (len(curr_text) != 0):
                    self.tokenized_text.append("".join(curr_text))
                    curr_text.clear() 

                if (text[pos] == '\n'):
                    self.tokenized_text.append(text[pos])
                    self.line_count += 1 


                pos += 1 

            elif (text[pos] == "("):
                if (len(curr_text) != 0):
                    self.tokenized_text.append("".join(curr_text))
                    curr_text.clear()

                pos = self.tokenize_brackets(text, pos)

            elif (text[pos] == '"'):
                if (len(curr_text) != 0):
                    self.tokenized_text.append("".join(curr_text))
                    curr_text.clear()

                pos = self.tokenize_quotes(text, pos)

            elif (text[pos] in Constants.SYMBOLS):
                if (len(curr_text) != 0):
                    self.tokenized_text.append("".join(curr_text))
                    curr_text.clear()

                symbolic_text, pos = self.tokenize_symbol(text, pos)
                self.tokenized_text.append(symbolic_text)


            else:
                curr_text.append(text[pos])
                pos += 1

        if len(curr_text) != 0:
            self.tokenized_text.append("".join(curr_text))
            curr_text.clear()







    
























