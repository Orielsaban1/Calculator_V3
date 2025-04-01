import re
from decimal import Decimal, getcontext

# Set precision for Decimal calculations
getcontext().prec = 28


# Define arithmetic operation functions
def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y


def power(x, y):
    return x ** y


def factorial(x):
    if x < 0:
        raise ValueError("Factorial is defined for non-negative integers only.")
    result = Decimal(1)
    for i in range(1, int(x) + 1):
        result *= i
    return result


# Map operator symbols to functions
OPERATORS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
    '^': power,
    '!': factorial
}


# Node Base Class
class Node:
    def evaluate(self):
        raise NotImplementedError("Subclasses must implement evaluate()")


# Concrete Node Classes
class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class UnaryOpNode(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def evaluate(self):
        return self.operator(self.operand.evaluate())


class BinaryOpNode(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self):
        return self.operator(self.left.evaluate(), self.right.evaluate())


# Parser Class
class Parser:
    def __init__(self, expression):
        # Tokenize the expression, allowing for unary operators and handling negative signs
        self.tokens = re.findall(r'\d+\.\d+|\d+|[' + re.escape(''.join(OPERATORS.keys())) + r']',
                                 expression.replace(' ', ''))
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected=None):
        token = self.current()
        if expected and token != expected:
            raise ValueError(f"Expected token '{expected}', got '{token}'")
        self.pos += 1
        return token

    def parse(self):
        node = self.parse_expr(0)
        if self.pos != len(self.tokens):
            raise ValueError(f"Unexpected token at end: {self.current()}")
        return node

    def parse_expr(self, min_prec):
        left = self.parse_term()
        while True:
            token = self.current()
            if token is None or token not in OPERATORS:
                break
            op = OPERATORS[token]
            left = self.handle_operator(op, left, min_prec)
        return left

    def handle_operator(self, op, left, min_prec):
        if op == factorial:
            return self.handle_unary(op, left)
        return self.handle_binary(op, left, min_prec)

    def handle_unary(self, op, left):
        self.consume()
        operand = self.parse_term()
        return UnaryOpNode(op, operand)

    def handle_binary(self, op, left, min_prec):
        cur_prec = 1  # Set appropriate precedence
        if cur_prec < min_prec:
            return left
        next_min = cur_prec + 1
        self.consume()
        right = self.parse_expr(next_min)
        return BinaryOpNode(op, left, right)

    def parse_term(self):
        token = self.current()
        if token == '-' or token == '+':
            op = OPERATORS[token]
            self.consume()
            operand = self.parse_factor()
            return UnaryOpNode(op, operand)
        return self.parse_factor()

    def parse_factor(self):
        token = self.current()
        if token.isdigit() or '.' in token:
            self.consume()
            return NumberNode(Decimal(token))
        elif token == '(':
            self.consume('(')
            node = self.parse_expr(0)
            self.consume(')')
            return node
        elif token == "!":  # Factorial operator
            self.consume("!")
            operand = self.parse_primary()
            return UnaryOpNode(OPERATORS["!"], operand)
        raise ValueError(f"Unexpected token: {token}")

    def parse_primary(self):
        token = self.current()
        if token is None:
            raise ValueError("Unexpected end of input")
        if re.match(r'^[+-]?\d+(\.\d+)?$', token):  # Matches optional sign with numbers
            self.consume()
            return NumberNode(Decimal(token))
        elif token == '(':
            self.consume('(')
            node = self.parse_expr(0)
            self.consume(')')
            return node
        raise ValueError(f"Unexpected token: {token}")


# Calculator Class
class Calculator:
    def __init__(self):
        self.operators = OPERATORS

    def evaluate(self, expression):
        parser = Parser(expression)
        tree = parser.parse()
        return tree.evaluate()


# Main Execution
if __name__ == '__main__':
    calculator = Calculator()
    while True:
        try:
            expr = input("Enter an equation: ").replace(" ", "")
            result = calculator.evaluate(expr)


