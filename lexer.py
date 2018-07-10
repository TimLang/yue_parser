
class Token:
    def __init__(self, token_type, literal, line_number):
        self._token_type = token_type
        self._literal = literal
        self._line_number = line_number

    @property
    def token_type(self):
        return self._token_type

    @token_type.setter
    def token_type(self, token_type):
        self._token_type = token_type

    @property
    def literal(self):
        return self._literal

    @literal.setter
    def literal(self, literal):
        self._literal = literal

    @property
    def line_number(self):
        return self._line_number

    @line_number.setter
    def line_number(self, line_number):
        self._line_number = line_number

    def __str__(self):
        return "{}: {}".format(self.token_type, self.literal)


class Lexer:

    def __init__(self, source_code):
        self._source_code = source_code
        self._position = 0
        self._read_position = 0
        self._line_count = 0
        self._ch = ''

        self.init_token_types()
        self.init_keywords_dict()

    def init_token_types(self):
        self.ILLEGAL = -2
        self.EOF = -1
        self.LET = 0
        self.IDENTIFIER = 1
        self.ASSIGN_SIGN = 2
        self.PLUS_SIGN = 3
        self.INTEGER = 4
        self.SEMICOLON = 5
        self.IF = 6
        self.ELSE = 7

        self.MINUS_SIGN = 8
        self.BANG_SIGN = 9
        self.ASTERISK = 10
        self.SLASH = 11
        self.LT = 12
        self.GT = 13
        self.COMMA = 14

        self.FUNCTION = 15
        self.TRUE = 16
        self.FALSE = 17
        self.RETURN = 18

        self.LEFT_BRACE = 19
        self.RIGHT_BRACE = 20
        self.EQ = 21
        self.NOT_EQ = 22
        self.LEFT_PARENT = 23
        self.RIGHT_PARENT = 24

    def init_keywords_dict(self):
        self._keywords_dict = {}
        self._keywords_dict["let"] = Token(self.LET, "let", 0)
        self._keywords_dict["if"] = Token(self.IF, "if", 0)
        self._keywords_dict["else"] = Token(self.ELSE, "else", 0)

        self._keywords_dict["fn"] = Token(self.FUNCTION, "fn", 0)
        self._keywords_dict["true"] = Token(self.TRUE, "true", 0)
        self._keywords_dict["false"] = Token(self.FALSE, "false", 0)
        self._keywords_dict["return"] = Token(self.RETURN, "return", 0)


    def read_char(self):
        if self._read_position >= len(self._source_code):
            self._ch = -1
        else:
            self._ch = self._source_code[self._read_position]

        self._read_position += 1

    def peek_char(self):
        if self._read_position >= len(self._source_code):
            return False
        else:
            return self._source_code[self._read_position]

    def skip_white_space_and_newline(self):
        while (self._ch == ' ' or self._ch == '\t' or self._ch == '\u00a0' or self._ch == '\n'):
            if (self._ch == '\t' or self._ch == '\n'):
                self._line_count+=1
            self.read_char()

    def read_identifier(self):
        identifier = ""
        while(self._ch.isalpha()):
            identifier += self._ch
            self.read_char()
        return identifier

    def read_number(self):
        number = ''
        while(self._ch.isdigit()):
            number += self._ch
            self.read_char()
        return number

    def next_token(self):
        token = None
        continue_read = True

        self.skip_white_space_and_newline()
        line_count = self._line_count
        self._position = self._read_position

        if(self._ch):
            if self._ch == self.EOF:
                token = Token(self.EOF, self._ch, line_count)
                self.continue_read = False
            elif self._ch == "=":
                peeked = self.peek_char()
                #check is a equal sign
                if peeked == '=':
                    pass
                else:
                    token = Token(self.ASSIGN_SIGN, self._ch, line_count)
            elif self._ch.isalpha():
                identifier = self.read_identifier()
                if identifier in self._keywords_dict:
                    token = self._keywords_dict[identifier]
                else:
                    token = Token(self.ILLEGAL, identifier, line_count)
            elif self._ch.isdigit():
                num = self.read_number()
                token = Token(self.INTEGER, num, line_count)
            else:
                token = Token(self.ILLEGAL, self._ch, line_count)

        if(continue_read):
            self.read_char()
        return token

    def lexing(self):
        tokens = []
        self.read_char()
        token = self.next_token()

        while(token is not None and (token.token_type != self.EOF)):
            tokens.append(token)
            token = self.next_token()

        [print(x) for x in tokens]


if __name__ == "__main__":
    lexer = Lexer("let a = 122;")
    lexer.lexing()