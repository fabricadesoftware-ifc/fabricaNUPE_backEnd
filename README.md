# NuPe
Projeto desenvolvido por membros da **Fábrica de Software IFC - Araquari** para melhorar o fluxo de atendimento da equipe do **Núcleo Pedagógico**.
# Membros
 - Eduardo da Silva (**Coordenador**)
 - Yuri (**Estagiário**)
 - Luis Carvalho (**Bolsista**)
 - Jorge (**Bolsista**)
 - Kauã (**Bolsista**)
# Boas práticas de commit
 - **Iniciar no modo imperativo**. Exemplo: "**Adicionar**", "**Remover**", "**Alterar**", "**Implementar**".
 Uma dica boa para facilitar a criação dos commits, é validá-los usando a seguinte frase: “**Se aplicado, esse commit vai**”
 - **Limite de 50 caracteres**
 - **Direto** e **explicativo**
 - **Capitalizar o conteúdo**. Exemplo: "**Adicionar funcionalidade x para blabla**" ao invés de "**adicionar funcionalidade x para blabla**"
 - **Ao final do conteúdo** do commit, adicionar "**. #n**", onde **n é o id da issue**
# Issues
 - O **título** da issue **deve ser breve** e **específico**, seguindo o padrão do commit, **deve iniciar no modo imperativo**
 - A **descrição** deve ser utilizada para **detalhar** o que precisa ser feito, **e se necessário**, como ser feito
 - O **assignee** **não é obrigatório na criação**, é utilizado para **especificar** um **"responsável"** para resolver a issue. 
 
	**Obs**.: Caso a issue que você for resolver **não** tiver um responsável, **torne-se ele**
 - # Labels
 - Utilize **backend** ou **frontend** para informar **onde** deverá ser implementada
 - Utilize **error** para informar que um erro **deve ser corrigido**
 - Utilize **implementation** para informar que você está **desenvolvendo a solução**
 - Utilize **test** para informar que você está **desenvolvendo os tests** da implementação
 - Utilize **refactor** para informar que você está **refatorando o código** dos tests ou da implementação
 - **todo** e **doing** são associados a issue **automaticamente pelo kanban do gitlab**
 
	 **Obs**.: Ao ser fechada, a issue **deve** conter as labels **backend** ou **frontend**, **implementation**, **test**, **refactor** (se necessário), e um **responsável**(assignee). 
Isso é **necessário** para ter um controle das etapas que foram realizadas, onde foi feito e por quem foi feito.
# Branches
Cada issue em andamento **deve ter uma branch associada à ela**.
Por isso, o nome da branch deve seguir a nomenclatura padrão do gitlab "**issue_id-titulo-da-issue**".

**Exemplo**: Para uma issue com id "**2**" e título "**criar model de curso**". A branch para se trabalhar nessa issue **deve** ser criada com o nome "**2-criar-model-de-curso**".
# Merge Request
- O **título** do merge request para **issues** seguirá o padrão do gitlab. "**Resolve <titulo_issue>**"
-  A **descrição** deve informar os **principais** fatos do que foi feito. Ao final, adicionar **Closes #issue_id**

	Exemplo de merge request:
	
	**Título**: Resolve "Criar model de localizacao"
	**Descrição**:
	
		Adicionado tabelas de Cidade, Estado e Localizacao
		
	    Adicionado tests para Cidade, Estado e Localizacao
	    
	    Atualizado README


		Closes #1**
	**Obs**.: O checkbox para remover a branch após o merge deve ser mantido como **checked**

# Boas práticas Python
A parte do backend do  projeto **deve** seguir as orientações estabelecidas pela regulamentação do pep8.

O desenvolvimento do backend **está** e **deverá continuar** seguindo conforme o artigo https://realpython.com/python-pep8/

# Inicialização  do backend
É necessário instalar a versão 3.6+ do Python e o Poetry para gerenciar as dependências do projeto.

### Instalando o Python
Verifique se já tem o Python instalado, se você usa GNU/Linux, provavelmente já possui alguma versão do Python instalada por padrão. Para conferir, abra o terminal e digite o seguinte comando:

`$ which python`

ou

`$ which python3`

que deve retornar algo como  `/usr/bin/python`. Isso significa que o Python está instalado nesse endereço.

Caso contrário, será necessário realizar a instalação. Para isso, com o terminal aberto digite o seguinte comando:

`$ sudo apt-get install python3.6`

(`Optional`) Para instalar o gerenciador de pacotes pip, digite o comando:

`$ sudo apt-get install python3-pip`

### Instalando o Poetry
É possível instalar o Poetry utilizando o gerenciador de pacotes  `pip`. Para isso, no terminal digite o comando:

`pip3 install --user poetry`

`echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.bashrc`

Para verificar se o Poetry foi instalado com sucesso, utilize o comando:

`poetry --version`

### Executando o projeto
Dentro do diretório do projeto execute os seguintes comandos:

`poetry install` - cria uma virtualenv e instala as dependências

`poetry shell` - entra na virtualenv 

`./manage.py migrate` - cria as tabelas no banco de dados

`./manage.py runserver` - inicia um servidor web para executar o projeto. Estará rodando no endereço: 127.0.0.1:8000 (`default`)
