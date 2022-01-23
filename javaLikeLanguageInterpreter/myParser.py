from tokenizer import Scanner
import syntaxTree


class Parser(object):

    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    def get_pos(self):
        return self.scanner.lexer.lineno

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_col_of(p),
                                                                                      p.type, p.value))
        else:
            print('At end of input')

    def p_program(self, p):
        """program : program_element 
                   | program program_element"""
        if len(p) == 2:
            p[0] = syntaxTree.Program([p[1]])
        else:
            p[0] = syntaxTree.Program(p[1].elements + [p[2]])

    def p_program_element(self, p):
        """program_element : declaration
                           | fundef 
                           | instruction"""
        p[0] = p[1]


    def p_declaration(self, p):
        """declaration : TYPE inits ';' 
                       | error ';' """
        if len(p) == 3:
            p[0] = syntaxTree.Declaration(None, None, self.get_pos())
        else:
            p[0] = syntaxTree.Declaration(p[1], p[2], self.get_pos())

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = syntaxTree.Init(syntaxTree.Variable(p[1], self.get_pos()), p[3], self.get_pos())


    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | return_instr
                       | compound_instr"""
        p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'
                       | PRINT error ';' """
        p[0] = syntaxTree.PrintInstruction(p[2], self.get_pos())

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = syntaxTree.LabeledInstruction(label=p[1], instruction=p[3], position=self.get_pos())

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = syntaxTree.Assignment(syntaxTree.Variable(p[1], self.get_pos()), p[3], self.get_pos())

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        elseInstruction = None
        if len(p) == 8:
            elseInstruction = p[7]

        p[0] = syntaxTree.IfElse(condition=p[3], instruction=p[5], else_instruction=elseInstruction, position=self.get_pos())

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = syntaxTree.While(p[3], p[5], self.get_pos())

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = syntaxTree.ReturnInstruction(p[2], self.get_pos())


    def p_declaration_or_instructions(self, p):
        """declarations_or_instructions : declarations_or_instructions declaration
                                        | declarations_or_instructions instruction
                                        | """
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1] + [p[2]]

    def p_compound_instr(self, p):
        """compound_instr : '{' declarations_or_instructions '}' """
        p[0] = syntaxTree.CompoundInstruction(p[2], self.get_pos())

    def p_condition(self, p):
        """condition : expression"""
        p[0] = syntaxTree.Condition(p[1], self.get_pos())

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        constType = None
        constVal = None
        if p[1].startswith('"'):
            constType = "string"
            constVal = p[1]
        elif "." in p[1]:
            constType = "float"
            constVal = float(p[1])
        else:
            constType = "int"
            constVal = int(p[1])
        p[0] = syntaxTree.Const(constType, constVal, self.get_pos())

    def p_variable(self, p):
        """variable : ID"""
        p[0] = syntaxTree.Variable(p[1], self.get_pos())

    def p_expression(self, p):
        """expression : const
                      | variable
                      | arithmetic_expr
                      | logical_expr
                      | comparison_expr
                      | '(' expression ')'
                      | '(' error ')'
                      | funcall """
        expression = None
        if len(p) == 4:
            expression = p[2]
        else:
            expression = p[1]

        if expression is syntaxTree.BinExpr:
            p[0] = expression
        else:
            p[0] = syntaxTree.UnaryExpr(value=expression, position=self.get_pos())

    def p_logical_expr(self, p):
        """logical_expr : expression AND expression
                       | expression OR expression
        """
        p[0] = syntaxTree.LogicalExpr(p[2], left=p[1], right=p[3], position=self.get_pos())

    def p_comparison_expr(self, p):
        """comparison_expr : expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
        """
        p[0] = syntaxTree.ComparisonExpr(p[2], left=p[1], right=p[3], position=self.get_pos())

    def p_arithmetic_expr(self, p):
        """arithmetic_expr : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
        """
        p[0] = syntaxTree.ArithmeticExpr(p[2], left=p[1], right=p[3], position=self.get_pos())


    def p_funcall(self, p):
        """funcall : ID '(' expr_list_or_empty ')' 
                   | ID '(' error ')' """
        p[0] = syntaxTree.Funcall(p[1], p[3], self.get_pos())

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = syntaxTree.Fundef(returnType=p[1], identifier=p[2], argumentList=p[4], instruction=p[6], position=self.get_pos())

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]

    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = syntaxTree.Argument(p[1], p[2], self.get_pos())




