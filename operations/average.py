from operations.operator import Operator
from statistics import mean as avg
class Average(Operator):
    def __init__(self, name: str, power: int, arity: int, side_oper: bool = False):
        super().__init__(name, power, arity, side_oper)

    def execute_operation(self, num1: float, num2: float) -> float:
            return avg([num1,num2])
