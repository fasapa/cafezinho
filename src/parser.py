# Gerador tabela de parser LALR
import ply.yacc as yacc

# Importa lista de tokens do lexer
from lexer import tokens

# Funções extras
import parserextra as Extra

# Tabela de símbolos e escopo
import symtab as Sym

# Representação intermediária
import ir as IR

# Definições gramaticais
start = 'Programa'

def p_Programa(p):
    """Programa : DeclFuncVar DeclProg"""
    # print("todos simbolos")
    # for s in p[1]:
    #     print('Symbol: {}'.format(s))
    p[0] = p[1] + p[2]

# Constroi lista de variáveis
def p_DeclFuncVar(p):
    """DeclFuncVar : Tipo ID DeclVar ';' DeclFuncVar
                   | Tipo ID '[' INTCONST ']' DeclVar ';' DeclFuncVar
                   | Tipo ID DeclFunc DeclFuncVar
                   | empty"""
    # Tipo ID DeclVar ';' DeclFuncVar
    if len(p) == 6:
        symbol = Sym.SymbolVar(p[2], p[1])
        # if symbol.check_inlist(p[3]) or symbol.check_inlist(p[5]):
        #     print("ERRO: Variável {} já declarada.".format(p[2]))
        #     sys.exit(1)
        # else:
        p[0] = [symbol] + Extra.set_symbol_list_type(p[1], p[3]) + p[5]

    # Tipo ID '[' INTCONST ']' DeclVar ';' DeclFuncVar
    elif len(p) == 9:
        symbol = Sym.SymbolVec(p[2], p[1], p[4])
        # if symbol.check_inlist(p[6]) or symbol.check_inlist(p[8]):
        #     print("ERRO: Variável {} já declarada.".format(p[2]))
        #     sys.exit(1)
        # else:
        p[0] = [symbol] + Extra.set_symbol_list_type(p[1], p[6]) + p[8]

    # Tipo ID DeclFunc DeclFuncVar
    elif len(p) == 5:
        symbol = Sym.SymbolFun(p[2], p[1], p[3])
        p[0] = [symbol] + p[4]

    # Vazio
    else:
        p[0] = []

# Monta lista de variáveis (não conhecemos os tipos)
def p_DeclVar(p):
    """DeclVar : ',' ID DeclVar
               | ',' ID '[' INTCONST ']' DeclVar
               | empty"""
    # ',' ID DeclVar
    if len(p) == 4:
        symbol = Sym.SymbolVar(p[2], None)
        # if symbol.check_inlist(p[3]):
        #     print("ERRO: Variável {} já declarada.".format(p[2]))
        #     sys.exit(1)
        # else:
        p[0] = [symbol] + p[3]

    # ',' ID '[' INTCONST ']' DeclVar
    elif len(p) == 7:
        symbol = Sym.SymbolVec(p[2], None, p[4])
        # if symbol.check_inlist(p[6]):
        #     print("ERRO: Variável {} já declarada.".format(p[2]))
        #     sys.exit(1)
        # else:
        p[0] = [symbol] + p[6]

    # empty
    else:
        p[0] = []               # Lista vazia, não há mais variáveis

def p_DeclProg(p):
    """DeclProg : PROGRAMA Bloco"""
    p[0] = [Sym.SymbolFun("main", Sym.SymType.INT, IR.Function(None, p[2]))]

# VERIFICAR POR PARAMETROS REPETIDOS
def p_DeclFunc(p):
    """DeclFunc : '(' ListaParametros ')' Bloco"""
    if p[2] == []:
        p[0] = IR.Function(None, p[4])
    else:
        p[0] = IR.Function(p[2], p[4])

def p_ListaParametrosEmpty(p):
    """ListaParametros : empty"""
    p[0] = []

def p_ListaParametros(p):
    """ListaParametros : ListaParametrosCont"""
    p[0] = p[1]

def p_ListaParametrosCont(p):
    """ListaParametrosCont : Tipo ID
                           | Tipo ID '[' ']'
                           | Tipo ID ',' ListaParametrosCont
                           | Tipo ID '[' ']' ',' ListaParametrosCont"""
    # Tipo ID
    if len(p) == 3:
        symbol = Sym.SymbolVar(p[2], p[1])
        p[0] = [symbol]

    # Tipo ID '[' ']'
    elif len(p) == 5 and p[3] == '[':
        symbol = Sym.SymbolVec(p[2], p[1], None)
        p[0] = [symbol]

    # Tipo ID ',' ListaParametrosCont
    elif len(p) == 5 and p[3] == ',':
        symbol = Sym.SymbolVar(p[2], p[1])
        p[0] = [symbol] + Extra.set_symbol_list_type(p[1], p[4])

    # Tipo ID '[' ']' ',' ListaParametrosCont"""
    elif len(p) == 7:
        symbol = Sym.SymbolVec(p[2], p[1], None)
        p[0] = [symbol] + Extra.set_symbol_list_type(p[1], p[6])

def p_Bloco(p):
    """Bloco : '{' ListaDeclVar ListaComando '}'
             | '{' ListaDeclVar '}'"""
    # '{' ListaDeclVar ListaComando '}'
    if len(p) == 5:
        p[0] = IR.Block(p[2], p[3])

    # '{' ListaDeclVar '}'
    elif len(p) == 4:
        #print(p[2][0])
        p[0] = IR.Block(p[2], None)

def p_ListaDeclVar(p):
    """ListaDeclVar : empty
                    | Tipo ID DeclVar ';' ListaDeclVar
                    | Tipo ID '[' INTCONST ']' DeclVar ';' ListaDeclVar"""
    # empty
    if len(p) == 2:
        p[0] = []

    # Tipo ID DeclVar ';' ListaDeclVar
    elif len(p) == 6:
        symbol = Sym.SymbolVar(p[2], p[1])
        p[0] = [symbol] + Extra.set_symbol_list_type(p[1], p[3]) + p[5]

    # Tipo ID '[' INTCONST ']' DeclVar ';' ListaDeclVar
    elif len(p) == 9:
        symbol = Sym.SymbolVec(p[2], p[1], p[4])
        p[0] = [symbol] + Extra.set_symbol_list_type(p[1], p[6]) + p[8]


def p_Tipo(p):
    """Tipo : INT
            | CAR"""
    # Determina o tipo da declaração
    if p[1] == 'int':
        ty = Sym.SymType.INT
    elif p[1] == 'car':
        ty = Sym.SymType.CAR
    p[0] = ty                 # Retorna "int" ou "car"


def p_ListaComando(p):
    """ListaComando : Comando
                    | Comando ListaComando"""
    # Comando
    if len(p) == 2:
        p[0] = [p[1]]

    # Comando ListaComando
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]

# Comando vazio, não faz nada
def p_ComandoVazio(p):
    """Comando : ';'"""
    pass

def p_ComandoRetorne(p):
    """Comando : RETORNE Expr ';'"""
    p[0] = IR.Retorne(p[2])

def p_ComandoLeia(p):
    """Comando : LEIA LValueExpr ';'"""
    p[0] = IR.Leia(p[2])

def p_ComandoEscrevaExpr(p):
    """Comando : ESCREVA Expr ';'"""
    p[0] = IR.Escreva(p[2])

def p_ComandoEscrevaString(p):
    """Comando : ESCREVA STRING ';'"""
    p[0] = IR.Escreva(p[2])

def p_ComandoNovalinha(p):
    """Comando : NOVALINHA ';'"""
    p[0] = IR.Novalinha()

def p_ComandoSe(p):
    """Comando : SE '(' Expr ')' ENTAO Comando
               | SE '(' Expr ')' ENTAO Comando SENAO Comando"""
    # SE '(' Expr ')' ENTAO Comando
    if len(p) == 7:
        p[0] = IR.Se(p[3], p[6])

    # SE '(' Expr ')' ENTAO Comando SENAO Comando
    elif len(p) == 9:
        p[0] = IR.Se(p[3], p[6], p[8])

def p_Commando(p):
    """Comando : Expr ';'
               | ENQUANTO '(' Expr ')' EXECUTE Comando
               | Bloco"""
    # Expr ';'
    if len(p) == 3:
        p[0] = IR.Eval(p[1])

    # ENQUANTO '(' Expr ')' EXECUTE Comando
    elif len(p) == 7:
        p[0] = IR.Enquanto(p[3], p[6])

    # Bloco
    elif len(p) == 2:
        p[0] = p[1]


def p_Expr(p):
    """Expr : AssignExpr"""
    p[0] = p[1]

def p_AssignExpr(p):
    """AssignExpr : CondExpr
                  | LValueExpr '=' AssignExpr"""
    # CondExpr
    if len(p) == 2:
        p[0] = p[1]

    # LValueExpr '=' AssignExpr
    elif len(p) == 4:
        p[0] = IR.Assign(p[1], p[3])


def p_CondExpr(p):
    """CondExpr : OrExpr
                | OrExpr '?' Expr ':' CondExpr"""
    # OrExpr
    if len(p) == 2:
        p[0] = p[1]

    # OrExpr '?' Expr ':' CondExpr
    elif len(p) == 6:
        p[0] = IR.TerOp(p[1], p[3], p[4])

def p_OrExpr(p):
    """OrExpr : OrExpr OU AndExpr
              | AndExpr"""
    # AndExpr OU EqExpr
    if len(p) == 4:
        p[0] = IR.LogOp(IR.LogOpType.OR, p[1], p[3])

    # AndExpr
    elif len(p) == 2:
        p[0] = p[1]

def p_AndExpr(p):
    """AndExpr : AndExpr E EqExpr
               | EqExpr"""
    # AndExpr E EqExpr
    if len(p) == 4:
        p[0] = IR.LogOp(IR.LogOpType.AND, p[1], p[3])

    # EqExpr
    elif len(p) == 2:
        p[0] = p[1]

def p_EqExprEQUAL(p):
    """EqExpr : EqExpr EQUAL DesigExpr
              | DesigExpr"""
    # EqExpr EQUAL DesigExpr
    if len(p) == 4:
        p[0] = IR.RelOp(IR.RelOpType.EQUAL, p[1], p[3])

    # DesigExpr
    elif len(p) == 2:
        p[0] = p[1]


def p_EqExprDIFF(p):
    """EqExpr : EqExpr DIFF DesigExpr"""
    p[0] = IR.RelOp(IR.RelOpType.DIFF, p[1], p[3])

def p_DesigExpr(p):
    """DesigExpr : DesigExpr '<' AddExpr
                 | DesigExpr '>' AddExpr
                 | AddExpr"""
    # DesigExpr '<' AddExpr
    if len(p) == 4 and p[2] == '<':
        p[0] = IR.RelOp(IR.RelOpType.LESS, p[1], p[3])

    # DesigExpr '<' AddExpr
    elif len(p) == 4 and p[2] == '>':
        p[0] = IR.RelOp(IR.RelOpType.BIGGER, p[1], p[3])

    # AddExpr
    elif len(p) == 2:
        p[0] = p[1]

def p_DesigExprGEQ(p):
    """DesigExpr : DesigExpr GEQ AddExpr"""
    p[0] = IR.RelOp(IR.RelOpType.BIGGEREQ, p[1], p[3])

def p_DesigExprLEQ(p):
    """DesigExpr : DesigExpr LEQ AddExpr"""
    p[0] = IR.RelOp(IR.RelOpType.LESSEQ, p[1], p[3])

def p_AddExpr(p):
    """AddExpr : AddExpr '+' MulExpr
               | AddExpr '-' MulExpr
               | MulExpr"""
    # AddExpr '+' MulExpr
    if len(p) == 4 and p[2] == '+':
        p[0] = IR.BinOp(IR.BinOpType.PLUS, p[1], p[3])

    # AddExpr '+' MulExpr
    elif len(p) == 4 and p[2] == '-':
        p[0] = IR.BinOp(IR.BinOpType.MINUS, p[1], p[3])

    # MulExpr
    elif len(p) == 2:
        p[0] = p[1]

def p_MulExpr(p):
    """MulExpr : MulExpr '*' UnExpr
               | MulExpr '/' UnExpr
               | MulExpr '%' UnExpr
               | UnExpr"""
    # MulExpr '*' UnExpr
    if len(p) == 4 and p[2] == '*':
        p[0] = IR.BinOp(IR.BinOpType.MULT, p[1], p[3])

    # MulExpr '/' UnExpr
    elif len(p) == 4 and p[2] == '/':
        p[0] = IR.BinOp(IR.BinOpType.DIV, p[1], p[3])

    # MulExpr '%' UnExpr
    elif len(p) == 4 and p[2] == '%':
        p[0] = IR.BinOp(IR.BinOpType.MOD, p[1], p[3])

    # UnExpr
    elif len(p) == 2:
        p[0] = p[1]

def p_UnExpr(p):
    """UnExpr : '-' PrimExpr
              | '!' PrimExpr
              | PrimExpr"""
    # '-' PrimExpr
    if len(p) == 3 and p[1] == '-':
        p[0] = IR.UnOp(IR.UnOpType.INV, p[2])

    # '!' PrimExpr
    elif len(p) == 3 and p[1] == '!':
        p[0] = IR.UnOp(IR.UnOpType.NEG, p[2])

    # PrimExpr
    elif len(p) == 2:
        p[0] = p[1]

def p_LValueExpr(p):
    """LValueExpr : ID '[' Expr ']'
                  | ID"""
    # ID '[' Expr ']'
    if len(p) == 5:
        p[0] = IR.VecAcc(p[1], p[3])

    # ID
    elif len(p) == 2:
        p[0] = IR.Var(p[1])

def p_PrimExpr(p):
    """PrimExpr : ID '(' ')'
                | ID '(' ListExpr ')'
                | ID '[' Expr ']'
                | '(' Expr ')'"""
    # ID '(' ')'
    if len(p) == 4 and p[2] == '(':
        p[0] = IR.Funcall(p[1], None)

    # ID '(' ListExpr ')'
    elif len(p) == 5 and p[2] == '(':
        p[0] = IR.Funcall(p[1], p[3])

    # ID '[' Expr ']'
    elif len(p) == 5 and p[2] == '[':
        p[0] = IR.VecAcc(p[1], p[3])

    # '(' Expr ')'
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]

def p_PrimExprCARCONST(p):
    """PrimExpr : CARCONST"""
    p[0] = IR.Car(p[1])

def p_PrimExprINTCONST(p):
    """PrimExpr : INTCONST"""
    p[0] = IR.Int(p[1])

def p_PrimExprID(p):
    """PrimExpr : ID"""
    p[0] = IR.Var(p[1])

def p_ListExpr(p):
    """ListExpr : AssignExpr
                | ListExpr ',' AssignExpr"""
    # AssignExpr
    if len(p) == 2:
        p[0] = [p[1]]

    # ListExpr ',' AssignExpr
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]

def p_Empty(p):
    """empty : """
    pass

def p_error(p):
    print("ERRO: Sintático (token '" + p.value + "'; linha: " + str(p.lineno) + ").")

# Monta o Parser
parser = yacc.yacc()

# while True:
#     try:
#         s = input('calc > ')
#     except EOFError:
#         break
#     if not s: continue
#     result = parser.parse(s)
#     print(result)
