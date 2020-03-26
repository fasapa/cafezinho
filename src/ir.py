from enum import Enum

# Programa é formado por uma lista de funções e tabela de simbolos (escopo)
# class Programa(object):

#     def __init__(self, scope, functions):
#         self.scope = scope
#         self.funcs = functions

# Função possui nome, parâmetros, corpo e cria um escopo
class Function(object):

    def __init__(self, parameters, body):
        self.parameters = parameters
        self.body = body

    # def setName(self, name):
    #     self.name = name

    def __str__(self):
        return 'FUNCTION({}, {})'.format(str(self.parameters), str(self.body))

# Bloco de código. Contem lista de declaração e comandos
class Block(object):
    def __init__(self, declvars, commands):
        self.declvars = declvars
        self.commands = commands

##### Comandos da linguagem: se, enquanto, escreva, ...
class Command(object):
    pass

# Sequencia de comandos (lista)
class Seq(Command):
    def __init__(self, commandList):
        self.cmdList = commandList

# Expressões que são comandos
class Eval(Command):
    def __init__(self, expr):
        self.expr = expr

# Retorne
class Retorne(Command):
    def __init__(self, expr):
        self.expr = expr

# Leia
class Leia(Command):
    def __init__(self, expr):
        self.expr = expr

# Escreva
class Escreva(Command):
    def __init__(self, expr):
        self.expr = expr

class Novalinha(Command):
    def __str__():
        return "Novalinha"

# SE e SENÃO. Se com2 = None então é um SE
class Se(Command):
    def __init__(self, cmpar, com1, com2 = None):
        self.cmpar = cmpar
        self.com1 = com1
        self.com2 = com2

# Enquanto repetição
class Enquanto(Command):
    def __init__(self, cmpar, com):
        self.cmpar = cmpar
        self.com = com

##### Expressões
class Expr(object):
    pass

# Atribuição
class Assign(Expr):
    def __init__(self, lvalue, expr):
        self.lvalue = lvalue
        self.expr = expr

# Tipos de operações lógicas
class LogOpType(Enum):
    AND = 1,
    OR  = 2

# Operações Lógicas
class LogOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

# Tipos de operações relacionais
class RelOpType(Enum):
    EQUAL = 1,
    DIFF = 2,
    LESS = 3,
    BIGGER = 4,
    LESSEQ = 5,
    BIGGEREQ = 6

# Operações relacionais
class RelOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

# Tipos de operadores binários
class BinOpType(Enum):
    PLUS = 1,
    MINUS = 2,
    MULT = 3,
    DIV = 4,
    MOD = 5

# Operações binárias
class BinOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

# Tipos de operadores unários
class UnOpType(Enum):
    NEG = 1,
    INV = 2

class UnOp(Expr):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

# Operador ternário
class TerOp(Expr):
    def __init__(self, comp, exp1, exp2):
        self.comp = comp
        self.exp1 = exp1
        self.exp2 = exp2

# Expressões primárias
# chamada de função, número, caractere, acesso vetor, e variável
class Funcall(Expr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

# Acesso a posição de um vetor
class VecAcc(Expr):
    def __init__(self, name, posExpr):
        self.name = name
        self.posexpr = posExpr

# Variável
class Var(Expr):
    def __init__(self, name):
        self.name = name

# Variável vetor (funcall)
# class VarVec(Expr):
#     def __init__(self, name):
#         self.name

# Caractere
class Car(Expr):
    def __init__(self, value):
        self.value = value

# Intconst
class Int(Expr):
    def __init__(self, value):
        self.value = value

# # Representação intermediária (Programa)
# class Programa:

#     # Programa possui uma lista de funções e variáveis globais (escopo)
#     # O inicio do programa é a função __main__
#     def __init__(self, escopo):
#         self.escopo = escopo
#         self.listFunc = listFunc

# class Function:

#     pass

# Variável
# class Var:
#     pass
