
from .node import Node

class Statement(Node):

    def __init__(self):
        self._type = type(self).__name__

    @property
    def type_name(self):
        return self._type

    @property
    def token_iteral(self):
        return self._token_iteral

class LetStatement(Statement):
    def __init__(self, props={}):
        super(Statement, self)
        self._token = props.get('token')
        self._name = props.get('identifier')
        self._value = props.get('expression')
        self._token_iteral = """This is a Let statement, left is an identifer: {},  right size is value of {}""".format(self._name, self._value)

class ReturnStatement(Statement):
    def __init__(self, props={}):
        super(Statement, self)
        self._token = props.get('token')
        self._expression = props.get('expression')
        self._token_iteral = """Return with {}""".format(self._expression)

class ExpressionStatement(Statement):
    def __init__(self, props={}):
        super(Statement, self)

class BlockStatement(Statement):
    def __init__(self, props={}):
        super(Statement, self)
