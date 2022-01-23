class TreeNode(object):

    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.visit(self)


class Program(TreeNode):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
        self.children = elements


class Assignment(TreeNode):
    def __init__(self, variable, expression, position):
        super().__init__()
        self.variable = variable
        self.expression = expression
        self.children = [expression]
        self.position = position


class Declaration(TreeNode):
    def __init__(self, declType, inits, position):
        super().__init__()
        self.declType = declType
        self.inits = inits
        self.children = inits
        self.position = position


class Variable(TreeNode):
    def __init__(self, identifier, position):
        super().__init__()
        self.identifier = identifier
        self.children = []
        self.position = position


class Argument(TreeNode):
    def __init__(self, type, identifier, position):
        super().__init__()
        self.type = type
        self.identifier = identifier
        self.children = []
        self.position = position


class Const(TreeNode):
    def __init__(self, valueType, value, position):
        super().__init__()
        self.valueType = valueType
        self.value = value
        self.children = []
        self.position = position


class While(TreeNode):
    def __init__(self, condition, instruction, position):
        super().__init__()
        self.condition = condition
        self.instruction = instruction
        self.children = [condition, instruction]
        self.position = position


class Repeat(TreeNode):
    def __init__(self, instructions, condition, position):
        super().__init__()
        self.instructions = instructions
        self.condition = condition
        self.children = [condition, instructions]
        self.position = position


class Fundef(TreeNode):
    def __init__(self, returnType, identifier, argumentList, instruction, position):
        super().__init__()
        self.returnType = returnType
        self.identifier = identifier
        self.argumentList = argumentList
        self.instruction = instruction
        self.position = position

        self.children = [argumentList, instruction]


class Funcall(TreeNode):
    def __init__(self, identifier, args, position):
        super().__init__()
        self.identifier = identifier
        self.args = args
        self.children = args
        self.position = position


class PrintInstruction(TreeNode):
    def __init__(self, expression, position):
        super().__init__()
        self.expression = expression
        self.children = [expression]
        self.position = position


class LabeledInstruction(TreeNode):
    def __init__(self, label, instruction, position):
        super().__init__()
        self.label = label
        self.instruction = instruction
        self.children = [instruction]
        self.position = position


class IfElse(TreeNode):
    def __init__(self, condition, instruction, else_instruction, position):
        super().__init__()
        self.condition = condition
        self.instruction = instruction
        self.elseInstruction = else_instruction
        self.position = position

        self.children = [condition, instruction]
        if else_instruction is not None:
            self.children += [else_instruction]


class Condition(TreeNode):
    def __init__(self, expression, position):
        super().__init__()
        self.expression = expression
        self.position = position

        self.children = [expression]


class Init(TreeNode):
    def __init__(self, variable, expression, position):
        super().__init__()
        self.variable = variable
        self.expression = expression
        self.position = position

        self.children = [expression]


class ReturnInstruction(TreeNode):
    def __init__(self, return_expression, position):
        super().__init__()
        self.returnExpression = return_expression
        self.position = position

        self.children = [return_expression]


class CompoundInstruction(TreeNode):
    def __init__(self, declarations_or_instructions, position):
        super().__init__()
        self.declarations_or_instructions = declarations_or_instructions
        self.position = position

        self.children = declarations_or_instructions


class UnaryExpr(TreeNode):
    def __init__(self, value, position):
        super().__init__()
        self.value = value
        self.position = position

        self.children = [value]


class BinExpr(TreeNode):
    def __init__(self, op, left, right, position):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
        self.position = position

        self.children = [left, right]


class ArithmeticExpr(BinExpr):
    def __init__(self, op, left, right, position):
        super().__init__(op, left, right, position)
        self.op = op
        self.left = left
        self.right = right
        self.position = position

        self.children = [left, right]


class ComparisonExpr(BinExpr):
    def __init__(self, op, left, right, position):
        super().__init__(op, left, right, position)
        self.op = op
        self.left = left
        self.right = right
        self.position = position

        self.children = [left, right]


class LogicalExpr(BinExpr):
    def __init__(self, op, left, right, position):
        super().__init__(op, left, right, position)
        self.op = op
        self.left = left
        self.right = right
        self.position = position

        self.children = [left, right]

