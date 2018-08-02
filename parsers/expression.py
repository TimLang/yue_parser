
from .node import Node

class Expression(Node):
    def __init__(self, props={}):
        super(Expression, self)
        self._token = props.get('token')
        self._token_iteral = props.get('token_iteral')

    # @property
    # def literal(self):
        # return self._token_iteral

    def __str__(self):
        return self._token_iteral

class Identifier(Expression):
    def __init__(self, props={}):
        super(Identifier, self).__init__(props)

class PrefixExpression(Expression):
    def __init__(self, props={}):
        super(PrefixExpression, self).__init__(props)
        self._operator = props.get('operator')
        self._right = props.get('expression')
        self._token_iteral = """({}{})""".format(self._operator, self._right)

class InfixExpression(Expression):
    def __init__(self, props={}):
        super(InfixExpression, self).__init__(props)
        self._left_expression = props.get('left_expression')
        self._operator = props.get('operator')
        self._right_expression = props.get('right_expression')
        self._token_iteral = """({} {} {})""".format(self._left_expression, self._operator, self._right_expression)

class IntegerLiteral(Expression):
    def __init__(self, props={}):
        super(IntegerLiteral, self).__init__(props)

class Boolean(Expression):
    def __init__(self, props={}):
        super(Boolean, self).__init__(props)

class IfExpression(Expression):
    def __init__(self, props={}):
        super(IfExpression, self).__init__(props)

