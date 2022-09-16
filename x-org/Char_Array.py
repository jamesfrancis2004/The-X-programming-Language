
class Char_Array:
    
    def __init__(self, name, decl_text):
        self.name = name
        self.type = "char[]"
        self.decl_text = decl_text

    def return_string(self):
        return f"char* {self.name} = {self.decl_text};\n"
