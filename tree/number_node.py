from tree.node import Node
class NumberNode(Node):
    def __init__(self, value: float):
        self.value = value

    def execute_operation(self) -> float:
        return self.value