import string

from tml.common.position import Position
from tml.common.tokens import LBRACE, RBRACE, LSQBRACE, RSQBRACE, LPAREN, RPAREN, PLUS, MINUS, MUL, DIV, Token, EOF, \
    INT, FLOAT, KW, IDENT, EQ, STRING, COLON, COMMA, DER, EQEQ, GTEQ, GREATER, LESSEQ, LESS, NOTEQ
from tml.errors.lexical_errors import InvalidCharacterError

SIMPLE_CASES = {
    "{": LBRACE,
    "}": RBRACE,
    "[": LSQBRACE,
    "]": RSQBRACE,
    "(": LPAREN,
    ")": RPAREN,
    "+": PLUS,
    "-": MINUS,
    "*": MUL,
    "/": DIV,
    "=": EQ,
    ":": COLON,
    ",": COMMA
}

DIGITS = string.digits
DIGITS_DOT = DIGITS + "."

ASCII_LETTERS = string.ascii_letters
ASCII_LETTERS_UNDERSCORE = ASCII_LETTERS + "_"
ASCII_LETTERS_UNDERSCORE_DIGITS = ASCII_LETTERS_UNDERSCORE + DIGITS

LETTERS = string.ascii_letters
PUNCTUATIONS = string.punctuation
WHITE_SPACES = string.whitespace

KEYWORDS = ("let", "ret", "dict", "from", "import", "as")


def build_number(lexer):
    nod = 0
    res = lexer.current_char
    while lexer.current_char is not None and lexer.current_char in DIGITS_DOT:
        lexer.move_next()
        if lexer.current_char == ".":
            nod += 1
            if nod > 1:
                lexer.position_error_start = lexer.index.copy()
                lexer.position_error_end = lexer.position_error_start
                return None, InvalidCharacterError(lexer.file_name, lexer.position_error_start,
                                                   lexer.position_error_end, "'.' is not expected.")
            res += "."
        if lexer.current_char is not None and lexer.current_char in DIGITS:
            res += lexer.current_char
    if nod == 0:
        return Token(INT, res), None
    return Token(FLOAT, res), None


def build_ident(lexer):
    res = ""

    while lexer.current_char is not None and lexer.current_char in ASCII_LETTERS_UNDERSCORE_DIGITS:
        res += lexer.current_char
        lexer.move_next()

    if res in lexer.keywords:
        return Token(KW, res), None
    return Token(IDENT, res), None


def build_eq(lexer_object):
    res = ""
    lexer_object.start_position = lexer_object.index.copy()
    while lexer_object.current_char in ["=", ">"]:
        res += lexer_object.current_char
        lexer_object.move_next()
    if res == "=>":
        return Token(DER), None
    if res == "=":
        return Token(EQ), None
    if res == "==":
        return Token(EQEQ), None
    lexer_object.end_position = lexer_object.index.copy()
    message = "unexpected character."
    return InvalidCharacterError(lexer_object.file_name, lexer_object.start_position, lexer_object.end_position,
                                 message)


def build_compare(lexer_object):
    res = ""
    lexer_object.start_position = lexer_object.index.copy()
    while lexer_object.current_char in ("=", ">", "<"):
        res += lexer_object.current_char
        lexer_object.move_next()
    if res == ">=":
        return Token(GTEQ), None
    if res == ">":
        return Token(GREATER), None
    if res == "<=":
        return Token(LESSEQ), None
    if res == "<":
        return Token(LESS), None
    lexer_object.end_position = lexer_object.index.copy()
    message = "unexpected character."
    return InvalidCharacterError(lexer_object.file_name, lexer_object.start_position, lexer_object.end_position,
                                 message)


def build_not_eq(lexer_object):
    res = ""
    lexer_object.start_position = lexer_object.index.copy()
    while lexer_object.current_char in ("=", "!"):
        res += lexer_object.current_char
        lexer_object.move_next()
    if res == "!=":
        return Token(NOTEQ), None
    lexer_object.end_position = lexer_object.index.copy()
    message = "'=' or '!' is expected."
    return InvalidCharacterError(lexer_object.file_name, lexer_object.start_position, lexer_object.end_position,
                                 message)


def build_string(lexer_object):
    res = ""
    number_of_double_quote = 1
    lexer_object.move_next()
    while lexer_object.current_char is not None and lexer_object.current_char in LETTERS + DIGITS + PUNCTUATIONS + WHITE_SPACES and number_of_double_quote == 1:
        if lexer_object.current_char == "\"":
            number_of_double_quote += 1
            lexer_object.move_next()
        elif lexer_object.current_char == "\\":
            slash = lexer_object.current_char
            lexer_object.move_next()
            if lexer_object.current_char is not None and lexer_object.current_char == "\"":
                res = res + slash + '\"'
                lexer_object.move_next()
            else:
                res = res + slash + lexer_object.current_char  # noqa
                lexer_object.move_next()
        else:
            res = res + lexer_object.current_char
            lexer_object.move_next()
    return Token(STRING, res.rstrip("\n")), None


class Lexer:
    def __init__(self, keywords=KEYWORDS, simple_cases=None):
        if simple_cases is None:
            simple_cases = SIMPLE_CASES
        self.simple_cases = simple_cases
        self.keywords = keywords

        self.tokens = []
        self.current_char = None
        self.position_error_start = None
        self.position_error_end = None
        self.build_funcs = []

        self.file_name = None
        self.input_str = None
        self.index = None

    def m_plus(self, condition, build_func):
        self.build_funcs.append((condition, build_func))
        return self

    def move_next(self):
        self.index.move_next(self.current_char)
        if self.index.index < len(self.input_str):
            self.current_char = self.input_str[self.index.index]
        else:
            self.current_char = None

    def append_token(self, token):
        token.start_position.file_name = self.file_name
        token.end_position.file_name = self.file_name
        self.tokens.append(token)

    def tokenize(self, input_str, file_name):

        self.input_str = input_str
        self.file_name = file_name
        self.index = file_name == "<stdin>" and Position(file_name, input_str) or Position(file_name)
        self.move_next()

        def token_from_build_funcs():
            for condition, build_func in self.build_funcs:
                if condition(self.current_char):
                    start_position = self.index.copy()
                    token, error = build_func(self)
                    end_position = self.index.copy()
                    if token:
                        token.start_position = start_position
                        token.end_position = end_position
                        self.append_token(token)
                        return True, None
                    else:
                        if file_name == "<stdin>":
                            error.content = input_str
                        return None, error
            return False, None

        while self.current_char is not None:
            token_start_position = self.index.copy()
            if self.current_char in self.simple_cases:
                token_end_position = self.index.copy()
                self.append_token(Token(self.simple_cases[self.current_char], start_position=token_start_position,
                                        end_position=token_end_position))
                self.move_next()
            else:
                res, error = token_from_build_funcs()
                if error:
                    return None, error
                res or self.move_next()
        self.append_token(Token(EOF, value=None, start_position=self.index.copy(), end_position=self.index.copy()))
        return self.tokens, None
