import unittest
from interpreter_app.interpreter_engine import SimpleInterpreterFactory

class SimpleInterpreterFactoryTests(unittest.TestCase):
    def setUp(self):
        self.interpreter_factory = SimpleInterpreterFactory()

    def test_arithmetic_expression(self):
        equation = "3 + 5 * 2 - 4 / 2"
        context = {}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertEqual(result, 11)

    def test_complex_arithmetic_expression(self):
        equation = "(3 + 5) * (2 - 4 / 2) + 10"
        context = {}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertEqual(result, 10)

    def test_power_operation(self):
        equation = "2 ** 3 + 1"
        context = {}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertEqual(result, 9)

    def test_invalid_syntax_expression(self):
        equation = "3 + * 5"
        context = {}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        with self.assertRaises(Exception):
            interpreter.interpret()

    def test_regex_match_expression(self):
        equation = 'Regex(ATTR, ".*dog.*")'
        context = {"ATTR": "I have a Dog"}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertTrue(result)

    def test_regex_no_match_expression(self):
        equation = 'Regex(ATTR, ".*dog.*")'
        context = {"ATTR": "I have a cat"}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertFalse(result)

    def test_case_insensitive_regex_match(self):
        equation = 'Regex(ATTR, "(?i).*dog.*")'
        context = {"ATTR": "I have a DOG"}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertTrue(result)

    def test_numeric_string_handling_in_context(self):
        equation = "ATTR + 5"
        context = {"ATTR": "10"}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertEqual(result, 15)

    def test_nested_expression_with_context_variable(self):
        equation = "ATTR * (5 + 3)"
        context = {"ATTR": 2}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertEqual(result, 16)

    def test_multiple_regex_patterns(self):
        equation = 'Regex(ATTR, ".*cat.*|.*dog.*")'
        context = {"ATTR": "I have a dog and a cat"}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertTrue(result)

    def test_regex_with_special_characters(self):
        equation = 'Regex(ATTR, "^\\d{3}-\\d{2}-\\d{4}$")'
        context = {"ATTR": "123-45-6789"}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertTrue(result)

    def test_regex_no_match_with_special_characters(self):
        equation = 'Regex(ATTR, "^\\d{3}-\\d{2}-\\d{4}$")'
        context = {"ATTR": "123-456-789"}
        lexer = self.interpreter_factory.create_lexer(equation)
        parser = self.interpreter_factory.create_parser(lexer, context)
        interpreter = self.interpreter_factory.create_interpreter(parser, context)
        result = interpreter.interpret()
        self.assertFalse(result)

