from abc import ABC,abstractmethod

class Operator(ABC):
    def __init__(self, name: str, power: int, arity: int, side_oper: bool = False):
        self.name = name
        self.power = power
        self.arity = arity
        self.side_oper = side_oper

    @abstractmethod
    def execute_operation(self, *args: float) -> float:
        pass
