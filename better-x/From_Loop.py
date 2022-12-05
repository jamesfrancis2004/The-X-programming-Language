class From_Loop:

    def __init__(self, variable_name, start, end, step, scope):
        self.variable_name = variable_name
        self.start = start
        self.end = end
        self.step = step
        self.scope = scope

    def return_string(self):
        return f"for (int {self.variable_name} = {self.start}; {self.variable_name} < {self.end}; {self.variable_name} += {self.step}) {self.scope.return_string()}\n"


