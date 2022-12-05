
class If:
    
    def __init__(self, text, scope):
        self.text = text
        self.scope = scope


    def return_string(self):
        return f"if {self.text} {self.scope.return_string()}"

