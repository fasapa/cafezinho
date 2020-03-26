from enum import Enum
import json

# Categorias de símbolos
class SymCategory(Enum):
    VAR = 1
    VEC = 2
    FUN = 3

# Tipo do símbolo
class SymType(Enum):
    INT = 1
    CAR = 2

##### Símbolos
class Symbol:
    def __init__(self, name, category, symtype):
        self.name = name
        self.category = category
        self.symtype = symtype

    def __str__(self):
        if self.category == SymCategory.VEC:
            return 'SYMBOL({}[{}], {}, {}, index {})'.format(
                self.name, self.size, str(self.category), str(self.symtype), self.index)
        elif self.category == SymCategory.VAR:
            return 'SYMBOL({}, {}, {}, index {})'.format(
                self.name, str(self.category), str(self.symtype), self.index)
        else:
            return 'SYMBOL({}, {}, {})'.format(
                self.name, str(self.category), str(self.symtype))

    def check_inlist(self, inlist):
        for s in inlist:
            if self.name == s.name:  # Se está na lista
                return True
        return False            # Caso não esteja

    def setIndex(self, index):
        self.index = index

class SymbolVar(Symbol):
    def __init__(self, name, symtype):
        super().__init__(name, SymCategory.VAR, symtype)
        self.index = 0
        self.scope = 0

class SymbolVec(Symbol):
    def __init__(self, name, symtype, size):
        super().__init__(name, SymCategory.VEC, symtype)
        self.size = size
        self.index = 0

class SymbolFun(Symbol):
    def __init__(self, name, symtype, code):
        super().__init__(name, SymCategory.FUN, symtype)
        self.code = code

##### Tabela de símbolos
class Symtab:

    def __init__(self, parent = None):
        if parent:
            self.parent = id(parent)
        else:
            self.parent = None
        self.symbols = {}
        self.level = 0

    def add(self, name, symbol):
        self.symbols[name] = symbol

    # # Luke I'm your father!
    def setParent(self, parent):
        self.parent = id(parent)

    # Busca variável na tabela local.
    def lookup_local(self, var):
        return self.symbols.get(var)

    def setLevel(self, level):
        self.level = level

    def __str__(self):
        s = " PARENT: {}, LEVEL: {}, SYMBOLS:\n".format(str(self.parent), str(self.level))
        for var in self.symbols:
            s += '   {}\n'.format(str(self.symbols[var]))
        return s

# Escopo global
class Scope:
    """Deve existir apenas uma instancia desta classe durante a execução do
    compilador."""

    def __init__(self):
        self.table = {}

    def new(self, sId, table):
        self.table[id(sId)] = table
        return table

    def symtab(self, sId):
        return self.table[id(sId)]

    def getParent(self, table):
        return self.table[table.parent]

    def getGlobal(self):
        for tab in list(self.table.values()):
            if tab.parent == None:
                return tab

    def getVarTable(self, table, var):
        sym = table.lookup_local(var)

        while True:
            if sym != None:
                return table
            if table.parent == None:
                return None

            table = self.table[table.parent]
            sym = table.lookup_local(var)

    def lookup(self, table, var):
        sym = table.lookup_local(var)

        while True:
            if sym != None:
                return sym
            if table.parent == None:
                return None

            table = self.table[table.parent]
            sym   = table.lookup_local(var)


    def __str__(self):
        s = ""
        for t in self.table:
            s += '{}:{}'.format(str(t), str(self.table[t]))
        return s
