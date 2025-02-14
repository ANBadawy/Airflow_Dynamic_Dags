from abc import ABC, abstractmethod
import re

###############################################################################
# TOKEN TYPES AND FACTORIES                                                   #
###############################################################################

# Token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, REGEX, COMMA, STRING, ID, POWER = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF', 'REGEX', 'COMMA', 'STRING', 'ID', 'POWER'
)


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    __repr__ = __str__


class TokenFactory(ABC):
    @abstractmethod
    def create_token(self, type_, value):
        pass


class SimpleTokenFactory(TokenFactory):
    def create_token(self, type_, value):
        return Token(type_, value)


###############################################################################
# LEXER                                                                       #
###############################################################################

class Lexer:
    def __init__(self, text, token_factory):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.token_factory = token_factory

    def error(self):
        raise Exception(f'Invalid character: {self.current_char}')

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return float(result) if '.' in result else int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return self.token_factory.create_token(REGEX if result == 'Regex' else ID, result)

    def string(self):
        self.advance()
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()
            return self.token_factory.create_token(STRING, result)
        self.error()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.token_factory.create_token(INTEGER, self.number())
            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()
            if self.current_char == '"':
                return self.string()
            if self.current_char == '+':
                self.advance()
                return self.token_factory.create_token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return self.token_factory.create_token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                if self.current_char == '*':
                    self.advance()
                    return self.token_factory.create_token(POWER, '**')
                return self.token_factory.create_token(MUL, '*')
            if self.current_char == '/':
                self.advance()
                return self.token_factory.create_token(DIV, '/')
            if self.current_char == '(':
                self.advance()
                return self.token_factory.create_token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return self.token_factory.create_token(RPAREN, ')')
            if self.current_char == ',':
                self.advance()
                return self.token_factory.create_token(COMMA, ',')

            self.error()
        return self.token_factory.create_token(EOF, None)


###############################################################################
# AST NODES AND FACTORIES                                                     #
###############################################################################

class AST(ABC):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.value = token.value


class String(AST):
    def __init__(self, token):
        self.value = token.value


class FuncCall(AST):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args


class SimpleASTNodeFactory:
    def create_bin_op(self, left, op, right):
        return BinOp(left, op, right)

    def create_num(self, token):
        return Num(token)

    def create_string(self, token):
        return String(token)

    def create_func_call(self, func_name, args):
        return FuncCall(func_name, args)


###############################################################################
# PARSER                                                                      #
###############################################################################

class Parser:
    def __init__(self, lexer, ast_node_factory, context):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.ast_node_factory = ast_node_factory
        self.context = context

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return self.ast_node_factory.create_num(token)
        elif token.type == STRING:
            self.eat(STRING)
            return self.ast_node_factory.create_string(token)
        elif token.type == ID:
            var_name = token.value
            if var_name in self.context:
                value = self.context[var_name]
                token = Token(INTEGER, value)  # Convert variable to number token
                self.eat(ID)
                return self.ast_node_factory.create_num(token)
            else:
                raise Exception(f"Variable '{var_name}' not found in context")
        elif token.type == REGEX:
            return self.function_call()
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            raise Exception(f"Unexpected token type: {token.type}")

    def power(self):
        """power : factor ('**' factor)*"""
        node = self.factor()

        while self.current_token.type == POWER:
            token = self.current_token
            self.eat(POWER)
            node = self.ast_node_factory.create_bin_op(left=node, op=token, right=self.factor())

        return node

    def power(self):
        """Handles the power operator with the highest precedence."""
        node = self.factor()

        while self.current_token.type == POWER:
            token = self.current_token
            self.eat(POWER)
            node = self.ast_node_factory.create_bin_op(left=node, op=token, right=self.factor())

        return node

    def term(self):
        """term : power ((MUL | DIV) power)*"""
        node = self.power()  # Call the power function here

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = self.ast_node_factory.create_bin_op(left=node, op=token, right=self.power())

        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = self.ast_node_factory.create_bin_op(left=node, op=token, right=self.term())

        return node

    def function_call(self):
        func_name = self.current_token.value
        self.eat(REGEX if func_name == 'Regex' else ID)
        self.eat(LPAREN)
        args = [self.expr()]
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            args.append(self.expr())
        self.eat(RPAREN)
        return self.ast_node_factory.create_func_call(func_name, args)

    def parse(self):
        return self.expr()


###############################################################################
# INTERPRETER                                                                 #
###############################################################################

class Interpreter:
    def __init__(self, parser, context=None):
        self.parser = parser
        self.context = context or {}

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')



    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        # Convert strings to integers or floats if possible
        if isinstance(left, str) and left.replace(".", "", 1).isdigit():
            left = float(left) if "." in left else int(left)
        if isinstance(right, str) and right.replace(".", "", 1).isdigit():
            right = float(right) if "." in right else int(right)

        if node.op.type == PLUS:
            return left + right
        elif node.op.type == MINUS:
            return left - right
        elif node.op.type == MUL:
            return left * right
        elif node.op.type == DIV:
            if right == 0:
                raise Exception("Division by zero")
            return left / right
        elif node.op.type == POWER:
            return left ** right

    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_FuncCall(self, node):
        if node.func_name == 'Regex':
            if len(node.args) != 2:
                raise Exception("Regex function expects exactly 2 arguments.")
            value, pattern = self.visit(node.args[0]), self.visit(node.args[1])
            match = re.search(pattern, value, re.IGNORECASE)
            return bool(match)
        raise Exception(f"Unknown function '{node.func_name}'")

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


###############################################################################
# INTERPRETER FACTORY                                                         #
###############################################################################

class SimpleInterpreterFactory:
    def create_lexer(self, text):
        token_factory = SimpleTokenFactory()
        return Lexer(text, token_factory)

    def create_parser(self, lexer, context):
        ast_node_factory = SimpleASTNodeFactory()
        return Parser(lexer, ast_node_factory, context)

    def create_interpreter(self, parser, context):
        return Interpreter(parser, context)


