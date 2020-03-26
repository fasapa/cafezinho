import sys
# Gerador Léxico

# Palavras reservadas
reservadas = {
    'int'       : 'INT',
    'car'       : 'CAR',
    'programa'  : 'PROGRAMA',
    'retorne'   : 'RETORNE',
    'leia'      : 'LEIA',
    'escreva'   : 'ESCREVA',
    'novalinha' : 'NOVALINHA',
    'se'        : 'SE',
    'entao'     : 'ENTAO',
    'senao'     : 'SENAO',
    'enquanto'  : 'ENQUANTO',
    'execute'   : 'EXECUTE',
    'ou'        : 'OU',
    'e'         : 'E'
}

# Lista de Tokens
tokens = [ 'ID', 'INTCONST', 'CARCONST', 'STRING',
           'EQUAL', 'DIFF', 'GEQ', 'LEQ'
] + list(reservadas.values())

# Caracteres literais, não possuem significado fora de sua representação
literals = ['[', ']', ';', ',', '{', '}', '(', ')',
            '=', '?', ':', '<', '>',
            '+', '-', '*', '/', '%', '!',
]

# Expressões regulares
t_EQUAL    = r'=='
t_DIFF     = r'!='
t_GEQ      = r'>='
t_LEQ      = r'<='
t_CARCONST = r'\'.\''

# Converte representação textual para numérica
def t_INTCONST(t):
    r'0|([1-9][0-9]*)'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'

    # Se for uma palavra reservada retorna o token correspondente
    t.type = reservadas.get(t.value, 'ID')
    return t

# Reconhece uma cadeia de caractere e remove as aspas.
def t_STRING(t):
    r'"[^"]+"'
    t.value = t.value[1:-1]

    # Retorna erro se cadeia ocupa mais de uma linha
    if t.value.find('\n') != -1:
        print("ERRO: CADEIA DE CARACTERES OCUPA MAIS DE UMA LINHA (linha " +
              str(t.lexer.lineno) + ").")
        sys.exit()
    else:
        return t

# Ignora comentários, mas mantem quantidade de linhas atualizado.
def t_COMMENT(t):
    r'/\*[^\*/]+(\*/)?'

    # Conta quantidade de linhas
    linhas = t.value.count('\n')

    # Verifica a ocorrência de */ ao final do comentário
    if t.value[len(t.value)-2:len(t.value)] != '*/':
        print("ERRO: COMENTÁRIO NAO TERMINA (linha " + str(t.lexer.lineno-linhas) + ").")
        sys.exit()
    else:
        # Atualiza número de linhas
        t.lexer.lineno += t.value.count('\n')
        pass

# Mantem informação sobre o número de linhas
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra especial do PLY. Ignora qualquer valor neste grupo (espaços e tab).
t_ignore = ' \t\r'

# Gerenciamento de erros para caracteres desconhecidos
def t_error(t):
    print("ERRO: CARACTERE INVÁLIDO: '%s'." % t.value[0])
    sys.exit()

# Gera o lexer
import ply.lex as lex
lexer = lex.lex()
