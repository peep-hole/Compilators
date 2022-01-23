import ply.lex as lex


class Scanner(object):

    def find_col_of(self, token):
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        return token.lexpos - last_cr

    def build(self):
        self.lexer = lex.lex(object=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    literals = "{}()<>=;:,+-*/%&|^"

    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'print': 'PRINT',
        'return': 'RETURN',
        'while': 'WHILE'
    }

    t_EQ = r"=="
    t_NEQ = r"!="
    t_LE = r"<="
    t_GE = r">="
    t_OR = r"\|\|"
    t_AND = r"&&"


    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_newline2(self, t):    # for return and newline purpose
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' in line {t.lexer.lineno}")
        t.lexer.skip(1)

    def t_LINE_COMMENT(self, t):
        r'\//.*'
        pass

    def t_FLOAT(self, t):
        r"\d+(\.\d*)|\.\d+"
        return t

    def t_INTEGER(self, t):
        r"\d+"
        return t

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        return t

    def t_TYPE(self, t):
        r"\b(int|float|string)\b"
        return t

    def t_ID(self, t):
        r"[a-zA-Z_]\w*"
        t.type = Scanner.reserved.get(t.value, 'ID')
        return t

    tokens = ["AND", "EQ", "FLOAT", "GE", "ID", "INTEGER", "LE", "NEQ", "OR",
              "STRING", "TYPE", ] + list(reserved.values())

    t_ignore = ' \t\f'




