# NuPe

Projeto desenvolvido por membros da **Fábrica de Software IFC - Araquari** para melhorar o fluxo de atendimento da equipe do **Núcleo Pedagógico**.

# Membros

-   Eduardo da Silva (**Coordenador**)
-   Yuri (**Estagiário**)
-   Luis Carvalho (**Bolsista**)
-   Jorge (**Bolsista**)
-   Kauã (**Bolsista**)

# Boas práticas de commit

-   **Iniciar no modo imperativo**. Exemplo: "**Adicionar**", "**Remover**", "**Alterar**", "**Implementar**".
    Uma dica boa para facilitar a criação dos commits, é validá-los usando a seguinte frase: “**Se aplicado, esse commit vai**”
-   **Limite de 50 caracteres**
-   **Direto** e **explicativo**
-   **Capitalizar o conteúdo**. Exemplo: "**Adicionar funcionalidade x para blabla**" ao invés de "**adicionar funcionalidade x para blabla**"
-   **Ao final do conteúdo** do commit, adicionar "**. #n**", onde **n é o id da issue**

# Issues

-   O **título** da issue **deve ser breve** e **específico**, seguindo o padrão do commit, **deve iniciar no modo imperativo**
-   A **descrição** deve ser utilizada para **detalhar** o que precisa ser feito, **e se necessário**, como ser feito
-   O **assignee** **não é obrigatório na criação**, é utilizado para **especificar** um **"responsável"** para resolver a issue.

        	**Obs**.: Caso a issue que você for resolver **não** tiver um responsável, **torne-se ele**

-   # Labels
-   Utilize **backend** ou **frontend** para informar **onde** deverá ser implementada
-   Utilize **error** para informar que um erro **deve ser corrigido**
-   Utilize **implementation** para informar que você está **desenvolvendo a solução**
-   Utilize **test** para informar que você está **desenvolvendo os tests** da implementação
-   Utilize **refactor** para informar que você está **refatorando o código** dos tests ou da implementação
-   **todo** e **doing** são associados a issue **automaticamente pelo kanban do gitlab**
    **Obs**.: Ao ser fechada, a issue **deve** conter as labels **backend** ou **frontend**, **implementation**, **test**, **refactor** (se necessário), e um **responsável**(assignee).
    Isso é **necessário** para ter um controle das etapas que foram realizadas, onde foi feito e por quem foi feito.

# Branches

Cada issue em andamento **deve ter uma branch associada à ela**.
Por isso, o nome da branch deve seguir a nomenclatura padrão do gitlab "**issue_id-titulo-da-issue**".

**Exemplo**: Para uma issue com id "**2**" e título "**criar model de curso**". A branch para se trabalhar nessa issue **deve** ser criada com o nome "**2-criar-model-de-curso**".

# Merge Request

-   O **título** do merge request para **issues** seguirá o padrão do gitlab. "**Resolve <titulo_issue>**"
-   A **descrição** deve informar os **principais** fatos do que foi feito. Ao final, adicionar **Closes #issue_id**

        	Exemplo de merge request:

        	**Título**: Resolve "Criar model de localizacao"
        	**Descrição**:

        		Adicionado tabelas de Cidade, Estado e Localizacao

        	    Adicionado tests para Cidade, Estado e Localizacao

        	    Atualizado README


    	Closes #1**
    **Obs**.: O checkbox para remover a branch após o merge deve ser mantido como **checked**
