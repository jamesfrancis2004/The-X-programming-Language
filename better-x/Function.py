class Function:
    def __init__(self, name, itype, scope, variables):
        self.name = name
        self.return_type = itype
        self.type = "operation"
        self.scope = scope
        self.variables = [variables]
        self.index = 0

    def return_string(self):
        if self.index == 0:
            string =  f"void {self.name}({self.variables[self.index]})"
            self.index += 1 
            string += f"{{\n {self.scope.return_string()} }}\n"
        else:
            string = f"{self.name}({self.variables[self.index]});\n"
            self.index += 1

        return string
            


        

