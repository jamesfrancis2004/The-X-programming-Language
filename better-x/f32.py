


class f32:
    def __init__(self, name, declaration_text):
        self.name = name
        self.declaration_text = [declaration_text]
        self.type = "f32"
        self.index = 0


    def redeclare_variable(self, declaration_text):
        self.declaration_text.append(declaration_text)

    def return_string(self):
        before_index = self.index
        dec_text = self.declaration_text[self.index]
        self.index += 1
        
        if self.declaration_text == None:
            return f"float {self.name}"
        else:
            if before_index == 0:
                return f"float {self.name} = {dec_text};\n"
            else:
                return f"{self.name} = {dec_text};\n"



 
