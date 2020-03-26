import sys

import symtab as Sym
import ir as IR

##### Verifica compatibilidade de tipos
def check_type(ir, scope):
    # Percorre pela lista de funções verificando tipos
    for decl in ir:
        if type(decl) == Sym.SymbolFun:
            check_type_func(decl, decl.code, scope)

# Verifica tipo da função
def check_type_func(fdecl, fcode, scope):
    check_type_block(fdecl.symtype, fcode.body, scope)

def check_type_block(ftype, block_ir, scope):
    # Verifica o tipo dos comandos no bloco
    for cmd in block_ir.commands:
        check_type_command(ftype, cmd, block_ir, scope)

def check_type_command(ftype, cmd_ir, parent, scope):
    table = scope.symtab(parent)
    cmdt = type(cmd_ir)

    if cmdt == IR.Retorne:
        # CondExpr
        ctype = check_type_cexpr(cmd_ir.expr, table, scope)
        if ftype != ctype:
            print("ERRO: Tipo incompatível retorno '{}' e função '{}'.".format(ctype,ftype))

    elif cmdt == IR.Eval or cmdt == IR.Escreva:
        check_type_expr(cmd_ir.expr, table, scope)
    # elif cmdt == IR.Leia:
    #     check_decl_vars_lexpr(cmd_ir.expr, table, scope)
    elif cmdt == IR.Se:
        #print(check_type_cexpr(cmd_ir.cmpar, table, scope))
        if check_type_cexpr(cmd_ir.cmpar, table, scope) != Sym.SymType.INT:
            print("ERRO: Tipo incompatível expressão lógica SE.")
            sys.exit(1)
        check_type_command(ftype, cmd_ir.com1, parent, scope)
        check_type_command(ftype, cmd_ir.com2, parent, scope)

    elif cmdt == IR.Enquanto:
        if check_type_expr(cmd_ir.cmpar, table, scope) != Sym.SymType.INT:
            print("ERRO: Tipo incompatível expressão lógica ENQUANTO.")
            sys.exit(1)

            check_type_command(ftype, cmd_ir.com, parent, scope)
    elif cmdt == IR.Block:
        check_type_block(ftype, cmd_ir, scope)

def check_type_expr(expr_ir, table, scope):

    if type(expr_ir) == IR.Assign:
        t1 = check_type_cexpr(expr_ir.lvalue, table, scope)
        t2 = check_type_expr(expr_ir.expr, table, scope)

        if t1 != t2:
            print(expr_ir.lvalue.name)
            print("ERRO: Tipo incompatível em expressão de atribuição.")
            sys.exit(1)
        else:
            return t1
    else:
        return check_type_cexpr(expr_ir, table, scope)

def check_type_cexpr(expr_ir, table, scope):
    exprt = type(expr_ir)

    if exprt == IR.Var or exprt == IR.VecAcc:
        return scope.lookup(table, expr_ir.name).symtype
    elif exprt == IR.Car:
        return Sym.SymType.CAR
    elif exprt == IR.Int:
        return Sym.SymType.INT
    elif exprt == IR.LogOp:
        t1 = check_type_cexpr(expr_ir.left, table, scope)
        #print("LOG {}".format(t1))
        t2 = check_type_cexpr(expr_ir.right, table, scope)
        if t1 != t2 or t1 == Sym.SymType.CAR or t2 == Sym.SymType.CAR:
            print("ERRO: Tipo incompatível em expressão lógica.")
            sys.exit(1)
        else:
            return t1

    elif exprt == IR.RelOp:
        t1 = check_type_cexpr(expr_ir.left, table, scope)
        #print("REL {}".format(t1))
        t2 = check_type_cexpr(expr_ir.right, table, scope)
        if t1 != t2 or t1 == Sym.SymType.CAR or t2 == Sym.SymType.CAR:
            print("ERRO: Tipo incompatível em expressão relacional.")
            sys.exit(1)
        else:
            return t1

    elif exprt == IR.BinOp:
        t1 = check_type_cexpr(expr_ir.left, table, scope)
        #print("BIN {}".format(t1))
        t2 = check_type_cexpr(expr_ir.right, table, scope)
        if t1 != t2 or t1 == Sym.SymType.CAR or t2 == Sym.SymType.CAR:
            print("ERRO: Tipo incompatível em expressão binária.")
            sys.exit(1)
        else:
            return t1

    elif exprt == IR.UnOp:
        t1 = check_type_cexpr(expr_ir.expr, table, scope)
        #print("UN {}".format(t1))
        if t1 == Sym.SymType.CAR:
            print("ERRO: Tipo incompatível em expressão unária.")
            sys.exit(1)
        else:
            return t1

    elif exprt == IR.TerOp:
        t1 = check_type_cexpr(expr_ir.comp, table, scope)
        #print("TER {}".format(t1))
        if t1 == Sym.SymType.CAR:
            print("ERRO: Tipo incompatível em expressão ternária (comparação).")
            sys.exit(1)

        t2 = check_type_expr(expr_ir.exp1, table, scope)
        t3 = check_type_cexpr(expr_ir.exp2, table, scope)
    elif exprt == IR.Funcall:
        t1 = check_type_funcall(expr_ir, table, scope)
        #print("FUN {}".format(t1))
        return t1

def check_type_funcall(f_ir, table, scope):
    return scope.lookup(table, f_ir.name).symtype

##### Verifica se todas as variáveis foram declaradas
def check_decl_vars(ir, scope):
    # Percorre pelas funções procurando por variáveis não declaradas
    for decl in ir:
        if type(decl) == Sym.SymbolFun:
            check_decl_vars_func(decl.code, scope)

# Busca variáveis não declaradas dentro da função
def check_decl_vars_func(fun_ir, scope):
    check_decl_vars_block(fun_ir.body, scope)

def check_decl_vars_block(block_ir, scope):
    for cmd in block_ir.commands:
        check_decl_vars_command(cmd, block_ir, scope)

def check_decl_vars_command(command_ir, parent, scope):
    table = scope.symtab(parent)
    cmdt = type(command_ir)

    if cmdt == IR.Eval or cmdt == IR.Retorne or cmdt == IR.Escreva:
        check_decl_vars_expr(command_ir.expr, table, scope)
    elif cmdt == IR.Leia:
        check_decl_vars_lexpr(command_ir.expr, table, scope)
    elif cmdt == IR.Se:
        check_decl_vars_expr(command_ir.cmpar, table, scope)
        check_decl_vars_command(command_ir.com1, parent, scope)
        check_decl_vars_command(command_ir.com2, parent, scope)
    elif cmdt == IR.Enquanto:
        check_decl_vars_expr(command_ir.cmpar, table, scope)
        check_decl_vars_command(command_ir.com, parent, scope)
    elif cmdt == IR.Block:
        check_decl_vars_block(command_ir, scope)

# Verifica variáveis não declaradas em expressẽs
def check_decl_vars_expr(expr_ir, table, scope):
    exprt = type(expr_ir)

    if exprt == IR.Assign:
        check_decl_vars_lexpr(expr_ir.lvalue, table, scope)
        check_decl_vars_expr(expr_ir.expr, table, scope)
    elif exprt == IR.LogOp:
        check_decl_vars_expr(expr_ir.left, table, scope)
        check_decl_vars_expr(expr_ir.right, table, scope)
    elif exprt == IR.RelOp:
        check_decl_vars_expr(expr_ir.left, table, scope)
        check_decl_vars_expr(expr_ir.right, table, scope)
    elif exprt == IR.BinOp:
        check_decl_vars_expr(expr_ir.left, table, scope)
        check_decl_vars_expr(expr_ir.right, table, scope)
    elif exprt == IR.UnOp:
        check_decl_vars_expr(expr_ir.expr, table, scope)
    elif exprt == IR.TerOp:
        check_decl_vars_expr(expr_ir.comp, table, scope)
        check_decl_vars_expr(expr_ir.exp1, table, scope)
        check_decl_vars_expr(expr_ir.exp2, table, scope)
    elif exprt == IR.Funcall:
        check_decl_vars_funcall(expr_ir, table, scope)
    elif exprt == IR.Var or exprt == IR.VecAcc:
        if not scope.lookup(table, expr_ir.name):
            print("Variáveis '{}' não declarada.".format(expr_ir.name))
            sys.exit(1)

# Verifica variáveis não declaradas em chamada de função
def check_decl_vars_funcall(funcall_ir, table, scope):

    # Nome da função
    if not scope.lookup(table, funcall_ir.name):
        print("Função '{}' não declarada.".format(funcall_ir.name))
        sys.exit(1)

    # Lista de argumentos
    for arg in funcall_ir.args:
        check_decl_vars_expr(arg, table, scope)

# Verifica variáveis não declaradas em l expressões
def check_decl_vars_lexpr(lexpr_ir, table, scope):
    if not scope.lookup(table, lexpr_ir.name):
        print("Variáveis '{}' não declarada.".format(lexpr_ir.name))
        sys.exit(1)

##### Constroi tabela de símbolos. Analisa precensa de variáveis repetidas.
def build_symbol_table(ir, scope):

    # Cria tabela global
    t = Sym.Symtab()

    # Percorre a lista de declarações (variáveis e funções construindo a tabela de símbolos)
    for decl in ir:
        # Verifica se já existe na tabela
        if not t.lookup_local(decl.name):
            # Variáveis Globais
            if decl.category == Sym.SymCategory.VAR or decl.category == Sym.SymCategory.VEC:
                t.add(decl.name, decl)

            # Funções
            elif type(decl) == Sym.SymbolFun:
                t.add(decl.name, decl)
                build_symbol_table_func(decl.code, t, scope)

        else:
            # LOCAL DA VARIÁVEL
            print("ERRO: (Escopo Global) Variável '{}' já declarada.".format(decl.name))
            sys.exit(1)

    # Adiciona tabela ao escopo
    scope.new(t, t)

# Constroi tabela de símbols da função, sua tabela é a tabela do bloco abaixo.
def build_symbol_table_func(func_ir, parent, scope):
    """Percorre corpo da função buscando por BLOCKS"""
    build_symbol_table_block(func_ir.body, parent, scope, func_ir.parameters)

# Pra cada Bloco constroi um escopo novo com pai `parent` e adiciona symbols extras
def build_symbol_table_block(blk_ir, parent, scope, symbols):
    """Constroi tabela de símbolo para um cloco"""

    # Nova tabela
    t = Sym.Symtab(parent)

    if symbols == None:
        symbols = []

    # Adiciona símbolos extras
    for s in symbols:
        if not t.lookup_local(s.name):  # Já está declarada?
            t.add(s.name, s)
        else:
            print("ERRO: (Escopo Bloco Extra) Variável '{}' já declarada.".format(s.name))

    # Adiciona variáveis do bloco
    for s in blk_ir.declvars:
        if not t.lookup_local(s.name):
            t.add(s.name, s)
        else:
            print("ERRO: (Escopo Bloco Local) Variável '{}' já declarada.".format(s.name))

    # Percorre comandos que contenham outros blocos
    if blk_ir.commands != None:
        for cmd in blk_ir.commands:
            if type(cmd) == IR.Block:
                build_symbol_table_block(cmd, blk_ir, scope, None)
            else:
                build_symbol_table_command(cmd, blk_ir, scope)

    # Finaliza construção do escopo
    scope.new(blk_ir, t)

def build_symbol_table_command(command_ir, parent, scope):
    # Comandos que podem criar escopo: bloco, se e enquanto.
    cmd_type = type(command_ir)

    if cmd_type == IR.Se:
        build_symbol_table_command(command_ir.com1, parent, scope)
        build_symbol_table_command(command_ir.com2, parent, scope)
    elif cmd_type == IR.Enquanto:
        build_symbol_table_command(command_ir.com, parent, scope)
    elif cmd_type == IR.Block:
        build_symbol_table_block(command_ir, parent, scope, None)
