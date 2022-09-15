
class Function: 
    def __init__(self, name,  itype,  scope):
        self.name = name
        self.type = itype
        self.scope = scope
        self.type_translation = {None : "void"}

    
    def return_string(self):
        string = ["void", self.name+"("]
        for idx, i in enumerate(self.scope.parameters.values()):
            if idx == len(self.scope.parameters.values()) - 1:
                string.append(i.return_string())
                continue

            string.append(i.return_string() + ",")

        function_title = " ".join(string) + ") {\n"

        return function_title + self.scope.return_string() + "}\n"


        


