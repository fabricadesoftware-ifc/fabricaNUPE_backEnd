# NuPe

  

Projeto desenvolvido por membros da **Fábrica de Software IFC - Araquari** para melhorar o fluxo de atendimento da equipe do **Núcleo Pedagógico**.

  

# Membros

  

- Eduardo da Silva (**Coordenador**)

  

- Yuri (**Estagiário**)

  

- Luis Carvalho (**Bolsista**)

  

- Jorge (**Bolsista**)

  

# Issues

  

- O **título** da issue **deve ser breve** e **específico**, seguindo o padrão do commit, **deve iniciar no modo imperativo**

- A **descrição** deve ser utilizada para **detalhar** o que precisa ser feito, **e se necessário**, como ser feito

- O **assignee**  **não é obrigatório na criação**, é utilizado para **especificar** um **"responsável"** para resolver a issue.

  

**Obs**.: Caso a issue que você for resolver **não** tiver um responsável, **torne-se ele**

  

# Labels

  

- Utilize **backend** ou **frontend** para informar **onde** deverá ser implementada

- Utilize **bugfix** para informar que um erro deve ser corrigido

- Utilize **hotfix** para informar que um **erro emergencial** deve ser corrigido

- Utilize **enhancement** para informar que você está **desenvolvendo a solução**

- Utilize **test** para informar que você está **desenvolvendo os tests** da implementação

- Utilize **refactor** para informar que você está **refatorando o código** dos tests ou da implementação

-  **todo** e **doing** são associados a issue **automaticamente pelo kanban do gitlab**

  

**Obs**.: Ao ser fechada, a issue **deve** conter as labels **backend** ou **frontend**, **enhancement**, **test**, **refactor** (se necessário), e um **responsável**(assignee). Isso é **necessário** para ter um controle das etapas que foram realizadas, onde foi feito e por quem foi feito.

  

# Branches

  

Cada issue em andamento **deve ter uma branch associada à ela**. Por isso, o nome da branch deve seguir a nomenclatura padrão do gitflow "**feature-titulo-da-issue**".

  

**Exemplo**: Para uma issue com título "**criar model de curso**". A branch para se trabalhar nessa issue **deve** ser criada com o nome "**feature-criar-model-de-curso**".

  

# Merge Request

  

- O **título** do merge request para **issues** seguirá o padrão do gitlab. "**Resolve <titulo_issue>**"

  

- A **descrição** deve informar os **principais** fatos do que foi feito. Ao final, adicionar **Closes #issue_id**

  

Exemplo de merge request:

  

```

  

Título: Resolve "Criar model de localizacao"

  

Descrição:

  

Adicionado tabelas de Cidade, Estado e Localizacao

  

Adicionado tests para Cidade, Estado e Localizacao

  

Atualizado README

  
  

Closes #1

  

```

  

**Obs**.: O checkbox para remover a **feature branch** após o merge deve ser mantido como **checked**

  

# Inicialização do backend

  

É necessário instalar Docker ([https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)) e Docker Compose ([https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/))

  

Após instalado, dentro do diretório do projeto, execute o comando para iniciar a aplicação:

`$ docker-compose up -d`

  

O backend estará executando no endereço `http://localhost:80` ou apenas `http://localhost`

  

Para executar os testes:

`$ docker-compose exec backend bash -c "./manage.py test"`

  

Para executar as migrações:

`$ docker-compose exec backend bash -c "./manage.py makemigrations && ./manage.py migrate"`

  

Para criar o superusuário padrão:

`$ docker-compose exec backend bash -c "./manage.py createsuperuser --noinput"`

  

Para parar a executação utilize:

`$ docker-compose down`