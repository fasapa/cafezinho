Instalação
----------

Pacotes necessários (Debian):
python3 e python3-pip

PIP
----
PIP é um gerenciador de pacotes do Python. Vamos instalar o pipenv, um
gerenciador de ambiantes de desenvolvimento. A ideia é isolar projetos
em ambiantes diferentes.

Instalação global do pipenv (todos os usuários do sistema tem acesso):
pip install pipenv

Instalação local (apenas um usuário tem acesso. É NECESSÁRIO ALTERAR O PATH
PARA INCLUIR A PASTA ~/.local/bin):
pip install --user pipenv

PIPENV
------
Na pasta que contem o arquivo Pipfile execute:
pipenv install

Para executar o programa rode:
pipenv shell

Depois execute o arquivo cafezinho com o input:
python3 src/cafezinho.py input.

---
Caso algum erro, sintático ou semântico, for encontrado o compilador irá
emitir um ERRO e finalizará a execuação. Caso esteja tudo correto nada
acontecerá. Os arquivos referentes a análise semântica são:
semantic.py (análise semântica), symtab.py (tabela de símbolos) e
ir.py (representação intermediária).

--
Descrição dos arquivos:

	cafezinho.py
programa de entrada, passa os argumentos para a função main

	main.py
Contém a função main do programa. Executa todos os passos do 
compilador, frontend e backend. O yacc (ply) é chamado pela função
yacc.parser.parse, gerando a representação intermediária. Depois o
compilador realiza vários passes pela análise semântica: constroi
a tabela de símbolos (Semantic.build_symbol_table), verifica declaração
de variáveis (Semantic.check_decl_vars) e verifica tipos (Semantic.check_type)
Após as checagens passa a IR para o gerador de MIPS (Codegen.gen)

	lexer.py
Análise léxica

	parser.py
Análise sintática e constroi a representação intermediária.

	parsertab.py e parser.out
Arquivo gerado pelo PLY, contem a tabela de pulos do análisador sintático.

	ir.py
Descrição (classes) dos nós da representação intermediária.

	symtab.py
Tabela de símbolos e definição e símbolos

	semantic.py
Análise semanticas (inclui construção da tabela e símbolos)

	codegen.py
Gerador de código MIPS. Infelizmente está incompleto: gera código para
expressões, atribuição e acesso de variáveis GLOBAIS tanto simples quanto vetores,
gera código para os comandos enquanto, se e escreva. Variáveis locais não
são geradas.