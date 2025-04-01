from operations.operator import Operator
from tree.node import Node
class UnaryOpNode(Node):
    def __init__(self, op: Operator, child: Node):
        self.op = op
        self.child = child

    def execute(self) -> float:
        return self.op.execute_operation(self.child.execute())

