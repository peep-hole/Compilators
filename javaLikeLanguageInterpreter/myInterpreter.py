import syntaxTree
from visit import on, when
import sys
sys.setrecursionlimit(10000)


class VariableSymbol(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):

    def __init__(self, parent, name, calledFunction): # parent scope and symbol table name
        self.parentScope = parent
        self.symbols = {}
        self.name = name
        self.calledFunction = calledFunction
        self.inLoop = False

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        if self.shallowGet(name) is None:
            self.symbols[name] = symbol
        else:
            raise ValueError

    def shallowGet(self, name):
        return self.symbols.get(name, None)

    def printAll(self):
        print(self.name, self.symbols)
        if self.parentScope is not None:
            self.parentScope.printAll()

    def get(self, name): # get variable symbol or fundef from <name> entry
        ourScopeSymbol = self.symbols.get(name, None)
        if self.parentScope is not None:
            parentScopeSymbol = self.getParentScope().get(name)
        else:
            parentScopeSymbol = None
        if ourScopeSymbol is None and parentScopeSymbol is None:
            return None

        if ourScopeSymbol is None:
            return parentScopeSymbol
        else:
            return ourScopeSymbol

    def getParentScope(self):
        return self.parentScope


class Memory:

    def __init__(self, memory=None):
        self.parentFrame = memory
        self.variables = {}
        if memory is None:
            self.index = 0
        else:
            self.index = memory.index + 1

    def get(self, name):
        if name not in self.variables:
            return self.parentFrame.get(name)
        return self.variables[name]

    def set(self, name, value):
        self.variables[name] = value
        if name in self.variables:
            self.variables[name] = value
        elif self.parentFrame:
            self.parentFrame.set(name, value)

    def update(self, name, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parentFrame:
            self.parentFrame.update(name, value)


class ReturnValueException(Exception):

    def __init__(self, value):
        self.value = value


class Interpreter(object):
    @on('node')
    def visit(self, node):
        return "not covered"

    @when(syntaxTree.Program)
    def visit(self, node):
        self.memory = Memory()
        self.functions = {}
        for element in node.elements:
            element.accept(self)

    @when(syntaxTree.Assignment)
    def visit(self, node):
        val = node.expression.accept(self)
        self.memory.update(node.variable.identifier, val)

    @when(syntaxTree.Const)
    def visit(self, node):
        if node.valueType == 'string':
            return node.value[1:-1]
        return node.value

    @when(syntaxTree.Variable)
    def visit(self, node):
        return self.memory.get(node.identifier)

    @when(syntaxTree.While)
    def visit(self, node):

        self.memory = Memory(self.memory)
        while node.condition.accept(self):
                node.instruction.accept(self)

        self.memory = self.memory.parentFrame

    @when(syntaxTree.Funcall)
    def visit(self, node):
        function = self.functions[node.identifier]
        memory = Memory()

        argVals = zip(function.argumentList, node.args)
        for argument, argVal in argVals:
            argName = argument.identifier
            memory.set(argName, argVal.accept(self))
        memory.parentFrame = self.memory
        self.memory = memory
        try:
            function.instruction.accept(self)
        except ReturnValueException as e:
            return e.value
        finally:
            self.memory = self.memory.parentFrame

        return None

    @when(syntaxTree.Fundef)
    def visit(self, node):
        self.functions[node.identifier] = node

    @when(syntaxTree.PrintInstruction)
    def visit(self, node):
        text = node.expression.accept(self)
        print(text)

    @when(syntaxTree.IfElse)
    def visit(self, node):
        cond = node.condition.accept(self)
        if cond:
            node.instruction.accept(self)
        else:
            if node.elseInstruction is not None:
                node.elseInstruction.accept(self)

    @when(syntaxTree.Condition)
    def visit(self, node):
        val = node.expression.accept(self)
        if val == 0:
            return False
        return True

    @when(syntaxTree.Declaration)
    def visit(self, node):
        for init in node.inits:
            init.accept(self)

    @when(syntaxTree.Init)
    def visit(self, node):
        val = node.expression.accept(self)
        self.memory.set(node.variable.identifier, val)

    @when(syntaxTree.ReturnInstruction)
    def visit(self, node):
        val = node.returnExpression.accept(self)
        raise ReturnValueException(val)

    @when(syntaxTree.CompoundInstruction)
    def visit(self, node):
        try:
            self.memory = Memory(self.memory)
            for sth in node.declarations_or_instructions:
                sth.accept(self)
        finally:
            self.memory = self.memory.parentFrame

    @when(syntaxTree.UnaryExpr)
    def visit(self, node):
        return node.value.accept(self)

    @when(syntaxTree.ArithmeticExpr)
    def visit(self, node):
        left_val = node.left.accept(self)
        right_val = node.right.accept(self)

        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            return left_val / right_val
        elif node.op == '%':
            return left_val % right_val

        return None

    @when(syntaxTree.ComparisonExpr)
    def visit(self, node):
        left_val = node.left.accept(self)
        right_val = node.right.accept(self)

        res = None

        if node.op == '<':
            res = left_val < right_val
        elif node.op == '<=':
            res = left_val <= right_val
        elif node.op == '==':
            res = left_val == right_val
        elif node.op == '!=':
            res = left_val != right_val
        elif node.op == '>':
            res = left_val > right_val
        elif node.op == '>=':
            res = left_val >= right_val

        if res:
            return 1
        return 0

    @when(syntaxTree.LogicalExpr)
    def visit(self, node):
        left_val = node.left.accept(self)
        right_val = node.right.accept(self)
        res = None

        if node.op == 'AND':
            res = left_val and right_val
        elif node.op == 'OR':
            res = left_val or right_val

        if res:
            return 1
        return 0





