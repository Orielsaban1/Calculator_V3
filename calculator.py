import re
from operations.const import OPERATORS
from tree.number_node import NumberNode
from tree.unary_op_node import UnaryOpNode
from tree.node import Node
from tree.binary_op_node import BinaryOpNode


class Parser:
    def __init__(self, expression: str):
        # עשה שימוש ב-regex כדי למצוא את כל הטוקנים (מספרים, אופרטורים, סוגריים)
        self.tokens = re.findall(r'\d+\.\d+|\d+|[' + re.escape(''.join(OPERATORS.keys())) + r'()]', expression)
        self.pos = 0

    def parse(self):
        # כל הזמן מתחילים בפרסר שיפרק את הביטוי
        return self.parse_expression()

    def parse_expression(self):
        # עיבוד ביטוי שיכול להכיל אופרטורים כמו + ו-
        node = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in OPERATORS.keys() and OPERATORS[
            self.tokens[self.pos]].arity == 2:
            op = OPERATORS[self.tokens[self.pos]]
            self.pos += 1
            right = self.parse_term()
            node = BinaryOpNode(op, node, right)
        return node

    def parse_term(self):
        # עיבוד אופרציות כמו *, /, ^, %
        node = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in OPERATORS.keys() and OPERATORS[
            self.tokens[self.pos]].arity == 2:
            op = OPERATORS[self.tokens[self.pos]]
            self.pos += 1
            right = self.parse_factor()
            node = BinaryOpNode(op, node, right)
        return node

    def parse_factor(self):
        # טיפול במקרים של פעולות יונריות או חד-צדדיות
        token = self.tokens[self.pos]
        if token in OPERATORS and OPERATORS[token].arity == 1:
            # אופרטור חד-צדדי
            op = OPERATORS[token]
            self.pos += 1
            if op.side_oper:
                return UnaryOpNode(op, self.parse_factor())  # הילד של האופרטור הוא אפס או אחד
            else:
                return UnaryOpNode(op, self.parse_primary())
        return self.parse_primary()

    def parse_primary(self):
        # כל מה שלא אופרטור, כלומר מספרים, סוגריים או ביטויים פנימיים
        token = self.tokens[self.pos]
        if token.isdigit() or '.' in token:
            self.pos += 1
            return NumberNode(float(token))
        elif token == '(':
            self.pos += 1
            node = self.parse_expression()
            self.pos += 1  # Consume ')'
            return node
        raise ValueError(f"Unexpected token: {token}")


class Calculator:
    def __init__(self):
        self.operations = OPERATORS

    def execute_operations(self, expr):
        parser = Parser(expr)
        tree = parser.parse()
        return tree.execute_operation()

    def execute(self, expr):
        return self.execute_operations(expr)


if __name__ == '__main__':
    calculator = Calculator()
    input_usr = input("Enter an equation: ").replace(" ", "")
    result = calculator.execute(input_usr)
    print("Result:", result)