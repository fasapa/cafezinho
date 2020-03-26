import sys

import parser as yacc
import symtab as Symtab
import semantic as Semantic
import codegen as Codegen

def main(inputFile):

    # Le o arquivo de input e chama o parser
    with open(inputFile, 'r') as file:
        data = file.read()

    # Representação intermediária
    ir = yacc.parser.parse(data)
    irgen = ir

    # Scopo contem uma lista de tabelas de símbolos
    scope = Symtab.Scope()

    # Constroi tabela de símbols, retorna nova arvore.
    Semantic.build_symbol_table(ir, scope)
    scopegen = scope

    print(scope)

    # Varifica variáveis não declaradas
    Semantic.check_decl_vars(ir, scope)

    # Verifica se os tipos são compatíveis
    Semantic.check_type(ir, scope)

    # Gera MIPS
    Codegen.gen(irgen, scopegen)