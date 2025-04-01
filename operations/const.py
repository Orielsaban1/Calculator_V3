from operations.power import Power
from operations.factorial import Factorial
from operations.negative import Negative
from operations.plus import Plus
from operations.minus import Minus
from operations.multiple import Multiple
from operations.divide import Divide
from operations.modulo import Modulo
from operations.minimum import Minimum
from operations.maximum import Maximum
from operations.average import Average
PLUS = Plus("plus",1,2,False)
MINUS = Minus("minus",1,2,False)
MULTIPLE=Multiple("multiple",2,2,False)
DIVIDE=Divide("divide",2,2,False)
POWER=Power("power",3,2,False)
MODULO=Modulo("modulo",2,4,False)
AVERAGE=Average("average",5,2,False)
MAXIMUM=Maximum("maximum",5,2,False)
MINIMUM=Minimum("minimum",5,2,False)
NEGATIVE=Negative("negative",6,2,True)
FACTORIAL=Factorial("factorial",7,2,True)
OPERATORS={
    "+":PLUS,
    "-":MINUS,
    "*":MULTIPLE,
    "/":DIVIDE,
    "^":POWER,
    "%":MODULO,
    "@":AVERAGE,
    "$":MAXIMUM,
    "&":MINIMUM,
    "~":NEGATIVE,
    "!":FACTORIAL
}
