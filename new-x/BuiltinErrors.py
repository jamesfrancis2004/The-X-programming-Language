import Errors


class BuiltinErrors:
    def expected_curly_brackets(self, split_lines, line_count):
        Errors.line_error(split_lines[line_count], line_count)
        Errors.println("Expected a '{' before start of if statement body")
        Errors.println("")




