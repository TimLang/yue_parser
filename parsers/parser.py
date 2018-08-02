
from .node import Node
from .expression import Identifier,  PrefixExpression, InfixExpression, IntegerLiteral, Boolean, IfExpression
from .statement import Statement, LetStatement, ReturnStatement, ExpressionStatement, BlockStatement

from lexer import Lexer

class Program():
    def __init__(self):
        self._statements = []

    @property
    def statements(self):
        return self._statements

class Parser():

    LOWEST = 0
    EQUALS = 1  # ==
    LESSGREATER = 2 # < or >
    SUM = 3
    PRODUCT = 4
    PREFIX = 5 #-X or !X
    CALL = 6  #myFunction(X)
    INDEX = 7 # getting item from array by index

    def __init__(self, lexer):
        self._lexer = lexer.lexing()
        self._token_pos = 0
        self._cur_token = None
        self._peek_token = None
        self.next_token()
        self.next_token()
        self.program = Program()
        self._precedences_dict = self.init_precedences_dict()

        self._prefix_parser_funcs = self.register_prefix_parser_funcs()
        self._infix_parser_funcs = self.register_infix_parser_funcs()

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
        elif token_type == self._lexer.RETURN:
            return self.parse_returnstatment()
        else:
            return self.parse_expression_statement()

    def parse_letstatement(self):
        stmt_dict = {}
        if not self.expect_peek(self._lexer.IDENTIFIER):
            return
        stmt_dict['identifier'] = Identifier({'token_iteral': self._cur_token.literal})
        if not self.expect_peek(self._lexer.ASSIGN_SIGN):
            return
        self.next_token()
        stmt_dict['expression'] = self.parse_expression(Parser.LOWEST)

        if not self.expect_peek(self._lexer.SEMICOLON):
            return

        return LetStatement(stmt_dict)

    def parse_returnstatment(self):
        stmt_dict = {}
        if not self.expect_peek(self._lexer.IDENTIFIER):
            return
        stmt_dict['expression'] = self.parse_expression(Parser.LOWEST)
        return ReturnStatement(stmt_dict)

    def parse_expression_statement(self):
        stmt_dict = {}
        stmt_dict['token'] = self._cur_token
        stmt_dict['expression'] = self.parse_expression(Parser.LOWEST)
        stmt = ExpressionStatement(stmt_dict)

        if self.peek_token_is(self._lexer.SEMICOLON):
            self.next_token()
        return stmt

    def parse_expression(self, precedence):
        func = None
        infix_expression = None
        try:
            func = self._prefix_parser_funcs[self._cur_token.token_type]
        except:
            pass
        if func:
            left_expression = func()
            if (not self.peek_token_is(self._lexer.SEMICOLON)) and (precedence < self._peek_precedence()):
                infix_expression = self._infix_parser_funcs[self._peek_token.token_type]
                if not infix_expression:
                    return left_expression
                self.next_token()
                left_expression = infix_expression(left_expression)
            return left_expression
        else:
            return None

    def peek_token_is(self, token_type):
        return self._peek_token.token_type == token_type

    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        else:
            return False

    def init_precedences_dict(self):
        precedences_dict = {}
        precedences_dict[self._lexer.EQ] = Parser.EQUALS
        precedences_dict[self._lexer.NOT_EQ] = Parser.EQUALS
        precedences_dict[self._lexer.LT] =Parser. LESSGREATER
        precedences_dict[self._lexer.GT] = Parser.LESSGREATER
        precedences_dict[self._lexer.PLUS_SIGN] = Parser.SUM
        precedences_dict[self._lexer.MINUS_SIGN] = Parser.SUM
        precedences_dict[self._lexer.SLASH] = Parser.PRODUCT
        precedences_dict[self._lexer.ASTERISK] = Parser.PRODUCT
        precedences_dict[self._lexer.LEFT_PARENT] = Parser.CALL
        precedences_dict[self._lexer.LEFT_BRACKET] = Parser.INDEX

        return precedences_dict

    def register_prefix_parser_funcs(self):
        tmp_dict = {}

        tmp_dict[self._lexer.IDENTIFIER] = self.create_identifier()
        tmp_dict[self._lexer.BANG_SIGN] = self.create_prefix_expression()
        tmp_dict[self._lexer.MINUS_SIGN] = self.create_prefix_expression()
        tmp_dict[self._lexer.TRUE] = self.create_boolean()
        tmp_dict[self._lexer.FALSE] = self.create_boolean()
        tmp_dict[self._lexer.INTEGER] = self.create_integer()

        return tmp_dict

    def register_infix_parser_funcs(self):
        tmp_dict = {}

        tmp_dict[self._lexer.PLUS_SIGN] = self.create_infix_expression()
        tmp_dict[self._lexer.MINUS_SIGN] = self.create_infix_expression()
        tmp_dict[self._lexer.SLASH] = self.create_infix_expression()
        tmp_dict[self._lexer.ASTERISK] = self.create_infix_expression()
        tmp_dict[self._lexer.EQ] = self.create_infix_expression()
        tmp_dict[self._lexer.NOT_EQ] = self.create_infix_expression()
        tmp_dict[self._lexer.LT] = self.create_infix_expression()
        tmp_dict[self._lexer.GT] = self.create_infix_expression()

        return tmp_dict

    def create_prefix_expression(self):
        return lambda: self._prepare_prefix_expression()

    def create_infix_expression(self):
        return lambda left_expression: self._prepare_infix_expression(left_expression)

    def create_identifier(self):
        return lambda: Identifier({ 'token' : self._cur_token.token_type, 'token_iteral': self._cur_token.literal })

    def create_boolean(self):
        return lambda: Boolean({ 'token' : self._cur_token.token_type, 'token_iteral': self._cur_token.literal })

    def create_integer(self):
        return lambda: IntegerLiteral({ 'token' : self._cur_token.token_type, 'token_iteral': self._cur_token.literal })

    def _prepare_prefix_expression(self):
        cur_tok = self._cur_token
        self.next_token()
        return PrefixExpression({'token' : cur_tok.token_type, 'operator' : cur_tok.literal, 'expression' : self.parse_expression(Parser.PREFIX) })

    def _prepare_infix_expression(self, left_expression):
        props = {}
        cur_tok = self._cur_token

        props['left_expression'] = left_expression
        props['operator'] = cur_tok.literal

        cur_precedence = self._current_precedence()
        self.next_token()
        props['right_expression'] = self.parse_expression(cur_precedence)

        return InfixExpression(props)

    def _peek_precedence(self):
        pd = self._precedences_dict.get(self._peek_token.token_type)
        if pd:
            return pd
        else:
            return Parser.LOWEST

    def _current_precedence(self):
        pd = self._precedences_dict.get(self._cur_token.token_type)
        if pd:
            return pd
        else:
            return Parser.LOWEST
