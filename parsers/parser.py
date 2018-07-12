
from .node import Node
from .expression import Expression, Identifier,  PrefixExpression, InfixExpression, IntegerLiteral, Boolean, IfExpression
from .statement import Statement, LetStatement, ReturnStatement, ExpressionStatement, BlockStatement

from lexer import Lexer

class Program():
    def __init__(self):
        self._statements = []

    @property
    def statements(self):
        return self._statements

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
                self.program.statements.append(stmt)
            self.next_token()
        return self.program

    def parse_statement(self):
        token_type = self._cur_token.token_type
        if token_type == self._lexer.LET:
            return self.parse_letstatement()
        if token_type == self._lexer.RETURN:
            return self.parser_returnstatment()

    def parse_letstatement(self):
        stmt_dict = {}
        if not self.expect_peek(self._lexer.IDENTIFIER):
            return
        stmt_dict['identifier'] = Identifier({ 'token': self._cur_token.literal})
        if not self.expect_peek(self._lexer.ASSIGN_SIGN):
            return
        if not self.expect_peek(self._lexer.INTEGER):
            return
        stmt_dict['expression'] = Expression({ 'token_iteral': self._cur_token.literal})

        return LetStatement(stmt_dict)

    def parser_returnstatment(self):
        stmt_dict = {}
        if not self.expect_peek(self._lexer.IDENTIFIER):
            return
        stmt_dict['expression'] = Expression({ 'token_iteral': self._cur_token.literal})
        return ReturnStatement(stmt_dict)

    def peek_token_is(self, token_type):
        return self._peek_token.token_type == token_type

    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        else:
            return False
