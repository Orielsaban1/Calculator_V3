from tree.node import Node
from operations.operator import Operator
class BinaryOpNode(Node):
    def __init__(self, op: Operator, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right

    def execute_operation(self) -> float:
        return self.op.execute_operation(self.left.execute_operation(), self.right.execute_operation())
