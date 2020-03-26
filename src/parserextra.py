from symtab import Symbol, SymCategory, SymType

# Funções extras utilizadas em parser.py que não pertencem ao PLY.
def set_symbol_list_type(ty, slist):
    # Lista atualizada
    ulist = []

    # Atualiza lista de variáveis com tipo
    for s in slist:
        s.symtype = ty
        ulist += [s]

    return ulist



