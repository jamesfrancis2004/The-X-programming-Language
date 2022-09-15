class Println:
    def __init__(self):
        self.text = []
        self.variables = []
        self.type_conversion = {"i32": "%d"}

    def update_variable(self, variable):
        self.text.append(self.type_conversion[variable.type])
        self.variables.append(variable.name)


    def return_string(self):
        string = 'printf("'
        for i in self.text:
            string += i
        string += '\\n"'
        for i in self.variables:
            string += ("," + i)

        return string + ");\n"




        

