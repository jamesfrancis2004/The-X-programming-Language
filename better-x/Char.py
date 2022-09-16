class Char:

    def __init__(self, name, declaration_text):
        self.name = name
        self.type = "char"
        self.declaration_text = declaration_text

    def return_string(self):
        return f"char {self.name} = {self.declaration_text};\n"
