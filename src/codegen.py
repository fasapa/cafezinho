# Gera MIPS no standard output
import symtab as Sym
import ir as IR


def gen(ir, scope):
    print(".text ##### INÍCIO. Variáveis globais")
    print("sw $s1, 0($sp) # Prepara pilha para variáveis globais")
    g = scope.getGlobal()

    index = 1 # Posição na variável
    for sym in ir:
        if sym.category == Sym.SymCategory.VAR:
            print("addiu %sp, %sp, -4 #[VAR {}] index {}".format(sym.name, index))
            scope.lookup(g, sym.name).setIndex(index)
            index = index + 1
        elif sym.category == Sym.SymCategory.VEC:
            print("addiu %sp, %sp, -{} #[VEC {}({})] index {}".format(4*sym.size, sym.name, sym.size, index))
            scope.lookup(g, sym.name).setIndex(index)
            index = index + sym.size
        else:
            print("##### Gerando função")
            gen_func(sym.code, scope)


def gen_func(f_ir, scope):
    table = scope.symtab(f_ir.body)
    table.setLevel(scope.getParent(table).level + 1) # Atualiza nível do escopo
    gen_block(f_ir.body, scope)


def gen_block(block_ir, scope):
    # Gera código para os comandos dentro do bloco
    for cmd in block_ir.commands:
        gen_cmd(cmd, block_ir, scope)


def gen_cmd(cmd_ir, parent, scope):
    table = scope.symtab(parent)
    cmdt = type(cmd_ir)

    if cmdt == IR.Eval:
        gen_expr(cmd_ir.expr, table, scope)
    elif cmdt == IR.Se:
        gen_se(cmd_ir, parent, table, scope)
    elif cmdt == IR.Enquanto:
        gen_enquanto(cmd_ir, parent, table, scope)
    elif cmdt == IR.Escreva:
        gen_escreva(cmd_ir.expr, table, scope)


def gen_escreva(expr, table, scope):
    if type(expr) != str:
        gen_expr(expr, table, scope)
        print("move $a0, $s0 #[ESCREVA] Imprima inteiro")
        print("li $v0, 1 #[ESCREVA] print")
        print("syscall")


def gen_enquanto(enquanto_ir, parent, table, scope):

    print("{}:".format("INICIO" + str(id(enquanto_ir))))
    print("#[ENQUANTO CMPAR {}] Avalia expressão comparação esquerda.".format(enquanto_ir.cmpar.op))
    gen_expr(enquanto_ir.cmpar.left, table, scope)

    print("sw $s0, 0(%sp) #[ENQUANTO CMPAR] Salva resultado da expressão a esquerda na pilha.".format(enquanto_ir.cmpar.op))  # Armazena resultado de left na pilha
    print("addiu $sp, $sp, -4")  # Aumenta pilha

    print("#[ENQUANTO CMPAR {}] Avalia expressão comparação direita.".format(enquanto_ir.cmpar.op))
    gen_expr(enquanto_ir.cmpar.right, table, scope)

    print("lw $t1, 4($sp) #[ENQUANTO CMPAR] Remove valor da expressão a esquerda da pilha.".format(enquanto_ir.cmpar.op))  # Copia valor da expressão a esquerda para t1.
    print("addiu %sp, %sp, 4")  # Diminui pilha

    se_op = enquanto_ir.cmpar.op
    if se_op == IR.RelOpType.EQUAL:
        print("beq $s0, $t1, {} #[ENQUANTO SALTO]".format("FIM" + str(id(enquanto_ir))))
    elif se_op == IR.RelOpType.DIFF:
        print("bne $s0, $t1, {} #[ENQUANTO SALTO]".format("FIM" + str(id(enquanto_ir))))
    elif se_op == IR.RelOpType.LESS:
        print("blt $s0, $t1, {} #[ENQUANTO SALTO]".format("FIM" + str(id(enquanto_ir))))
    elif se_op == IR.RelOpType.BIGGER:
        print("bgt $s0, $t1, {} #[ENQUANTO SALTO]".format("FIM" + str(id(enquanto_ir))))
    elif se_op == IR.RelOpType.LESSEQ:
        print("ble $s0, $t1, {} #[ENQUANTO SALTO]".format("FIM" + str(id(enquanto_ir))))
    elif se_op == IR.RelOpType.BIGGEREQ:
        print("bge $s0, $t1, {} #[ENQUANTO SALTO]".format("FIM" + str(id(enquanto_ir))))
    elif se_op == IR.LogOpType.AND:
        print("and $s0, $t1, {} #[ENQUANTO SALTO]".format("FIM" + str(id(enquanto_ir))))
    elif se_op == IR.LogOpType.OR:
        print("or $s0, $t1, {} #[ENQUANTO SALTO]".format("FIM" + str(id(enquanto_ir))))

    print("[ENQUANTO CORPO {}] Corpo do enquanto".format(enquanto_ir.cmpar.op))
    gen_cmd(enquanto_ir.com, parent, scope)

    print("b {} #[ENQUANTO] Loop".format("INICIO" + str(id(enquanto_ir))))
    print("{}: #[ENQUANTO] FIM".format("FIM" + str(id(enquanto_ir))))


def gen_se(se_ir, parent, table, scope):

    print("#[SE CMPAR {}] Avalia expressão comparação esquerda.".format(se_ir.cmpar.op))
    gen_expr(se_ir.cmpar.left, table, scope)

    print("sw $s0, 0(%sp) #[SE CMPAR {}] Salva resultado da expressão a esquerda na pilha".format(se_ir.cmpar.op))
    print("addiu $sp, $sp, -4")  # Aumenta pilha

    print("#[SE CMPAR {}] Avalia expressão comparação direita.".format(se_ir.cmpar.op))
    gen_expr(se_ir.cmpar.right, table, scope)

    print("lw $t1, 4($sp) #[SE CMPAR {}] Remove valor da expressão a esquerda da pilha.".format(se_ir.cmpar.op))  # Copia valor da expressão a esquerda para t1.
    print("addiu %sp, %sp, 4")  # Diminui pilha

    #print("#[SE SALTO] Prepara para o salto!".format(se_ir.cmpar.op))
    se_op = se_ir.cmpar.op
    if se_op == IR.RelOpType.EQUAL:
        print("beq $s0, $t1, {} #[SE SALTO]".format("ENTAO" + str(id(se_ir))))
    elif se_op == IR.RelOpType.DIFF:
        print("bne $s0, $t1, {} #[SE SALTO]".format("ENTAO" + str(id(se_ir))))
    elif se_op == IR.RelOpType.LESS:
        print("blt $s0, $t1, {} #[SE SALTO]".format("ENTAO" + str(id(se_ir))))
    elif se_op == IR.RelOpType.BIGGER:
        print("bgt $s0, $t1, {} #[SE SALTO]".format("ENTAO" + str(id(se_ir))))
    elif se_op == IR.RelOpType.LESSEQ:
        print("ble $s0, $t1, {} #[SE SALTO]".format("ENTAO" + str(id(se_ir))))
    elif se_op == IR.RelOpType.BIGGEREQ:
        print("bge $s0, $t1, {} #[SE SALTO]".format("ENTAO" + str(id(se_ir))))
    elif se_op == IR.LogOpType.AND:
        print("and $s0, $t1, {} #[SE SALTO]".format("ENTAO" + str(id(se_ir))))
    elif se_op == IR.LogOpType.OR:
        print("or $s0, $t1, {} #[SE SALTO]".format("ENTAO" + str(id(se_ir))))

    print("#[SE CMPAR {}] Senão".format(se_ir.cmpar.op))
    if se_ir.com2:
        gen_cmd(se_ir.com2, parent, scope)
    print("b {} #[SE SALTO] FIM".format("FIM" + str(id(se_ir))))

    print("{}: #[SE CMPAR {}] Então".format("ENTAO" + str(id(se_ir)), se_ir.cmpar.op))
    gen_cmd(se_ir.com1, parent, scope)

    print("{} #[SE] FIM:".format("FIM" + str(id(se_ir))))


def gen_expr(expr_ir, table, scope):
    exprt = type(expr_ir)

    if exprt == IR.BinOp:
        gen_binop(expr_ir, table, scope)
    elif exprt == IR.UnOp:
        gen_unop(expr_ir, table, scope)
    elif exprt == IR.Int:
        print("li $s0, {} #[IMEDIATO {}] Gerando imediato".format(expr_ir.value, expr_ir.value))
    elif exprt == IR.Var:
        gen_var(expr_ir, table, scope)
    elif exprt == IR.VecAcc:
        gen_var(expr_ir, table, scope)
    elif exprt == IR.Assign:
        gen_attr(expr_ir, table, scope)


def gen_attr(attr_ir, table, scope):
    # Gera expressão a direita
    gen_expr(attr_ir.expr, table, scope)

    # Gera atribuição a esquerda (1 = atribuição)
    gen_var(attr_ir.lvalue, table, scope, 1)


def gen_var(var_ir, table, scope, tipo = 0):
    var = scope.lookup(table, var_ir.name)
    vartab = scope.getVarTable(table, var_ir.name)

    if vartab.level == 0:
        # Variável global
        if var.category == Sym.SymCategory.VAR:
            if tipo == 0:
                print("lw $s0, {}($s1) # [VAR {}] Carrega variável global.".format(-(var.index-1)*4, var_ir.name))
            else:
                print("sw $s0, {}($s1) # [VAR {}] Armazena variável global.".format(-(var.index - 1) * 4, var_ir.name))
        elif var.category == Sym.SymCategory.VEC:
            print("##### [VAR ()] Calcula índice de acesso ao vetor")
            gen_expr(var_ir.posexpr, table, scope)
            print("addiu $s0, $s0, {} #[VAR ()] (p - 1 + indice ($s0))".format(var.index-1))
            print("li $t1, -4")
            print("mult $s0, $t1 #[VAR ()] (p - 1 + indice ($s0))*4")
            print("mflo $s0")
            print("add $l1, $s1, $s0 #[VAR ()] $l1 = (p - 1 + indice ($s0))*4($s1)")
            if tipo == 0:
                print("lw $s0, 0($l1) #[VAR {}] Carrega variável global vetor".format(var_ir.name))
            else:
                print("lw $s0, 0($l1) #[VAR {}] Armazena variável global vetor".format(var_ir.name))


def gen_binop(binop_ir, table, scope):

    print("#[BINOP {}] Gerando expressão a esquerda.".format(binop_ir.op))
    gen_expr(binop_ir.left, table, scope)  # Gera código para expressão a esquerda

    print("sw $s0, 0(%sp) #[BINOP {}] Salva resultado da expressão a esquerda na pilha.".format(binop_ir.op))
    print("addiu $sp, $sp, -4")              # Aumenta pilha

    print("#[BINOP {}] Gerando expressão a direita.".format(binop_ir.op))
    gen_expr(binop_ir.right, table, scope) # Gera código para expressão a direita

    print("lw $t1, 4($sp) #[BINOP {}] Remove valor da expressão a esquerda da pilha.".format(binop_ir.op))
    print("addiu %sp, %sp, 4")             # Diminui pilha

    if binop_ir.op == IR.BinOpType.PLUS:
        #print("#[BINOP] SOMA")
        print("add $s0, $s0, $t1 #SOMA")
    elif binop_ir.op == IR.BinOpType.MINUS:
        #print("#[BINOP] SUBTRAÇÃO")
        print("sub $s0, $s0, $t1 #SUBTRAÇÃO")
    elif binop_ir.op == IR.BinOpType.MULT:
        #print("#[BINOP] MULTIPLICAÇÃO")
        print("mult $s0, $t1 #MULTIPLICAÇÃO") # Mutiplicação $s0 * $t1
        print("mflo $s0")      # Extrai o resultado da multiplicação para o registrador $s0
    elif binop_ir.op == IR.BinOpType.DIV:
        #print("#[BINOP] DIVISÃO INTEIRA")
        print("div $s0, $t1 #DIVISÃO INTEIRA")  # $s0 / $t1
        print("mflo $s0")      # Divisão inteira
    elif binop_ir.op == IR.BinOpType.MOD:
        #print("#[BINOP] RESTO")
        print("div $s0, $t1 #DIVISÃO INTEIRA RESTO")  # $s0 / $t1
        print("mfhi $s0")      # Resto da divisão (mod)


def gen_unop(unop_ir, table, scope):

    #print("#[UNOP] Gerando expressão unária.")
    if unop_ir.op == IR.UnOpType.INV:
        gen_expr(unop_ir.expr, table, scope)
        print("li $t1, -1 #[UNOP] Inversão")
        print("mult $s0, $t1 #[UNOP] Inversão")
        print("mlfo $s0 #[UNOP] Inversão")
    elif unop_ir.op == IR.UnOpType.NEG:
        gen_expr(unop_ir.expr, table, scope)
        print("nor $s0, $s0, $s0 #[UNOP] Negação")

    #print("#[UNOP] Fim da operação unária")

def gen_relop(relop_ir, table, scope):

    print("#[RELOP] Início da operação relacional. Gerando expressão a esquerda.")
    gen_expr(relop_ir.left, table, scope)

    print("#[RELOP] Salva resultado da expressão a esquerda na pilha")
    print("sw $s0, 0(%sp)")  # Armazena resultado de left na pilha
    print("addiu $sp, $sp, -4")  # Aumenta pilha

    print("#[RELOP] Gerando expressão a direita.")
    gen_expr(relop_ir.right, table, scope)  # Gera código para expressão a direita

    print("#[RELOP] Remove valor da expressão a esquerda da pilha.")
    print("lw $t1, 4($sp)")  # Copia valor da expressão a esquerda para t1.
    print("addiu %sp, %sp, 4")  # Diminui pilha

    if relop_ir.op == IR.RelOpType.LESS:
        pass
