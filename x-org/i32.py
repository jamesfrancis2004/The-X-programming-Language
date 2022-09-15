class i32:
    def __init__(self, name, declaration_text):
        self.name = name
        self.declaration_text = declaration_text
        self.type = "i32"


    def return_string(self):

        if self.declaration_text == None:
            return f"int {self.name}"

        return f"int {self.name} = {self.declaration_text};\n"

    

