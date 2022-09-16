


class Block:
    def __init__(self, title_text, body):
        self.title_text = title_text
        self.body = body
        self.primitive_types = set(["str", "i32", "f32", "f64", "operation", "struct"])
        self.valid_var_types = set([])
    
    def __repr__(self):
        return f"Scope text = {self.title_text}\nScope body = {self.body}"
                


