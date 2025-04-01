import re
from decimal import Decimal, getcontext

# Set the precision for Decimal operations
getcontext().prec = 28

class Operator:
    def __init__(self, symbol, precedence, num_operands, is_unary, allow_unary=False, associativity="left"):
        self.symbol = symbol
        self.precedence = precedence
        self.num_operands = num_operands
        self.is_unary = is_unary
        self.allow_unary = allow_unary
        self.associativity = associativity

    def execute(self, *args):
        raise NotImplementedError("Subclasses must implement execute()")

class Plus(Operator):
    def __init__(self):
        super().__init__("+", 1, 2, False)
    def execute(self, left, right):
        return left + right

class Minus(Operator):
    def __init__(self):
        super().__init__("-", 1, 2, False, allow_unary=True)
    def execute(self, *args):
        if len(args) == 1:
            return -args[0]
        elif len(args) == 2:
            return args[0] - args[1]
        else:
            raise ValueError("Minus requires 1 or 2 operands")

class Multiply(Operator):
    def __init__(self):
        super().__init__("*", 2, 2, False)
    def execute(self, left, right):
        return left * right

class Divide(Operator):
    def __init__(self):
        super().__init__("/", 2, 2, False)
    def execute(self, left, right):
        if right == 0:
            raise ValueError("Division by zero")
        return left / right

class Power(Operator):
    def __init__(self):
        super().__init__("^", 3, 2, False, associativity="right")
    def execute(self, left, right):
        return left ** right

class Factorial(Operator):
    def __init__(self):
        super().__init__("!", 4, 1, True)
    def execute(self, operand):
        n = int(operand)
        if n < 0:
            raise ValueError("Factorial is defined for non-negative integers only")
        result = Decimal(1)
        for i in range(1, n + 1):
            result *= i
        return result

class Node:
    def evaluate(self):
        raise NotImplementedError("Subclasses must implement evaluate()")

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
        return self.operator.execute(self.operand.evaluate())

class BinaryOpNode(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
    def evaluate(self):
        return self.operator.execute(self.left.evaluate(), self.right.evaluate())

class Parser:
    def __init__(self, expression, operators):
        self.tokens = re.findall(r'\d+\.\d+|\d+|[' + re.escape(''.join(operators.keys())) + r'()]', expression)
        self.pos = 0
        self.operators = operators

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
        left = self.parse_prefix()
        while True:
            token = self.current()
            if token is None or token not in self.operators:
                break
            op = self.operators[token]
            if op.is_unary and not op.allow_unary:
                cur_prec = op.precedence
                if cur_prec < min_prec:
                    break
                self.consume()
                left = UnaryOpNode(op, left)
                continue
            cur_prec = op.precedence
            if cur_prec < min_prec:
                break
            next_min = cur_prec + 1 if op.associativity == "left" else cur_prec
            self.consume()
            right = self.parse_expr(next_min)
            left = BinaryOpNode(op, left, right)
        return left

    def parse_prefix(self):
        token = self.current()
        if token and token in self.operators and self.operators[token].allow_unary:
            op = self.operators[token]
            self.consume()
            operand = self.parse_prefix()
            return UnaryOpNode(op, operand)
        return self.parse_primary()

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

class Calculator:
    def __init__(self):
        self.operators = {
            "+": Plus(),
            "-": Minus(),
            "*": Multiply(),
            "/": Divide(),
            "^": Power(),
            "!": Factorial()
        }

    def evaluate(self, expression):
        parser = Parser(expression, self.operators)
        tree = parser.parse()
        return tree.evaluate()

if __name__ == '__main__':
    calculator = Calculator()
    while True:
        try:
            expr = input("Enter an equation: ").replace(" ", "")
            result = calculator.evaluate(expr)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
