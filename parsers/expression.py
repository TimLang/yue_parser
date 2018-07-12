
from .node import Node

class Expression(Node):
    def __init__(self, props={}):
        super(Node, self)
        self._token_iteral = props['token_iteral']

    # @property
    # def literal(self):
        # return self._token_iteral

    def __str__(self):
        return self._token_iteral

class Identifier(Expression):
    def __init__(self, props={}):
        super(Expression, self)
        self._token = props['token']

    def __str__(self):
        return self._token

class PrefixExpression(Expression):
    def __init__(self, props={}):
        super(Expression, self)

class InfixExpression(Expression):
    def __init__(self, props={}):
        super(Expression, self)

class IntegerLiteral(Expression):
    def __init__(self, props={}):
        super(Expression, self)

class Boolean(Expression):
    def __init__(self, props={}):
        super(Expression, self)

class IfExpression(Expression):
    def __init__(self, props={}):
        super(Expression, self)

