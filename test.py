
from lexer import Lexer
from parsers.parser import Parser

def test_lexing():
    source = """
        let a = 122;
        let b = 69;
        !x = 5;
        if ( x == 5 ) {
            x = 9;
        }
    """
    lexer = Lexer(source).lexing()
    tokens = lexer.tokens
    # [print(x) for x in tokens]
    assert len(tokens) == 28

def test_parsing_let_statement():
    source_code = """
        let a = 122;
        let b = 1;
    """
    lexer = Lexer(source_code)
    program = Parser(lexer).exec_program()

    [print(x) for x in lexer.tokens]
    # [print(x._token_iteral) for x in program.statements]

    print(program.statements[0].token_iteral)
    assert len(program._statements) == 2
    assert program.statements[0].token_iteral == "This is a Let statement, left is an identifer: a,  right size is value of 122"

def test_parsing_return_statement():
    source_code = """
        return a;
    """

    lexer = Lexer(source_code)
    program = Parser(lexer).exec_program()

    assert program.statements[0]._token_iteral == "Return with a"

def test_parsing_expression_statement():
    pass

def test_parsing_block_statement():
    pass

def test_parsing_prefix_expression():
    source_code = """
        !1;
    """

    lexer = Lexer(source_code)
    program = Parser(lexer).exec_program()

    print("===========\n")
    print(program.statements[0]._token_iteral)
    print("===========\n")

def test_parsing_infix_expression():
    source_code = """
    1+2*3
    """
    lexer = Lexer(source_code)
    program = Parser(lexer).exec_program()

    print("===========\n")
    print(program.statements[0]._token_iteral)
    print("===========\n")

def test_parsing_boolean():
    pass

def test_parsing_integer_literal():
    pass

def test_parsing_array_literal():
    pass

if __name__ == "__main__":

    test_lexing()

    test_parsing_let_statement()
    test_parsing_return_statement()
    test_parsing_expression_statement()
    test_parsing_block_statement()

    test_parsing_prefix_expression()
    test_parsing_infix_expression()
    test_parsing_integer_literal()
    test_parsing_array_literal()

