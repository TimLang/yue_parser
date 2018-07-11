
from lexer import Lexer

class Node:

    def __init__(self, prop={}):
        self._token_iteral = ""

    @property
    def token_iteral(self):
        return self._token_iteral

class Statement(Node):
    pass

class Expression(Node):
    def __init__(self, props={}):
        super(Node, self)
        self._token_iteral = props['token_iteral']

    def __str__(self):
        return self._token_iteral

class Identifier(Expression):
    def __init__(self, props={}):
        super(Expression, self)
        self._token = props['token']

    def __str__(self):
        return self._token

class LetStatement(Statement):
    def __init__(self, props={}):
        super(Statement, self)
        self._name = props['identifier']
        self._value = props['expression']
        self._token_iteral = """This is a Let statement, left is an identifer: {},  right size is value of {}""".format(self._name, self._value)

class Program():
    def __init__(self):
        self._statements = []

class Parser():
    def __init__(self, lexer):
        self._lexer = lexer.lexing()
        self._token_pos = 0
        self._cur_token = None
        self._peek_token = None
        self.next_token()
        self.next_token()
        self.program = Program()

    def next_token(self):
        self._cur_token = self._peek_token
        if self._token_pos < len(self._lexer.tokens):
            self._peek_token = self._lexer.tokens[self._token_pos]
            self._token_pos += 1

    def exec_program(self):
        while(self._cur_token.token_type != self._lexer.EOF):
            stmt = self.parse_statement()
            if stmt:
                self.program._statements.append(stmt)
            self.next_token()
        return self.program

    def parse_statement(self):
        token_type = self._cur_token.token_type
        if token_type == self._lexer.LET:
            return self.parse_letstatement()

    def parse_letstatement(self):
        lexer = self._lexer
        let_stmt_dict = {}
        if not self.expect_peek(lexer.IDENTIFIER):
            return
        let_stmt_dict['identifier'] = Identifier({ 'token': self._cur_token._literal})
        if not self.expect_peek(lexer.ASSIGN_SIGN):
            return
        if not self.expect_peek(lexer.INTEGER):
            return
        let_stmt_dict['expression'] = Expression({ 'token_iteral': self._cur_token._literal})

        return LetStatement(let_stmt_dict)

    def peek_token_is(self, token_type):
        return self._peek_token.token_type == token_type

    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        else:
            return False


if __name__ == "__main__":
    source_code = """
        let a = 122;
        let b = 69;
    """
    lexer = Lexer(source_code)
    program = Parser(lexer).exec_program()

    # [print(x._token_iteral) for x in program._statements]

    assert len(program._statements) == 2
    assert program._statements[0]._token_iteral == 'This is a Let statement, left is an identifer: a,  right size is value of 122'

