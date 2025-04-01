from abc import ABC,abstractmethod


class Node(ABC):
    @abstractmethod
    def execute_operation(self) -> float:
        pass
