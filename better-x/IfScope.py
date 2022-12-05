class IfScope:


    def __init__(self, variables):
        self.valid_var_types = {"i32", "f32", "f64",
                                "operation", "struct", 
                                "char[]",
                                "char",
                                "loop"}

        self.built_ins = set(["println"])
        self.variable_conversion = {"char": 8}
        self.body = []
        self.variables = variables

    def return_string(self):
        string = "{\n"
        for i in self.body:
            string +=  i.return_string()

        return string + "}\n"
