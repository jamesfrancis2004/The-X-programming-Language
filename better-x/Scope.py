

class Scope(object):
    def __init__(self, parameters, global_scope=False):
        self.parameters = parameters
        self.valid_var_types = {"i32", "f32", "f64",
                                "operation", "struct", 
                                "char[]",
                                "char",
                                "loop"}
        self.variable_conversion = {"char": 8}
        self.built_ins = set(["println"])

        self.variables = self.parameters.copy()
        self.body = []
        self.global_scope = global_scope


    def return_string(self):
        string = ""
        for i in self.body:
            string +=  i.return_string()

        return string
