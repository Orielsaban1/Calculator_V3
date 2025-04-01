from operations.operator import Operator
import math

class Factorial(Operator):
    def __init__(self, name: str, power: int, arity: int,side_oper: bool = False):
        super().__init__(name, power, arity, side_oper)

    def execute_operation(self, num: float) -> float:
        if int(num) != num:
            raise ValueError(f"The number {num} is not an integer")
        return math.factorial(int(num))