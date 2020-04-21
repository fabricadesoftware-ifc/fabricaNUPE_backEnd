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

# Criação de Issues

 - O título da issue **deve ser breve** e **específico**, seguindo o padrão do commit, **deve iniciar no modo imperativo**
 - A descrição deve ser utilizada para **detalhar** o que precisa ser feito, **e se necessário**, como ser feito
 - O campo assignee não é obrigatório na criação, é utilizado para especificar um "**responsável**" para resolver a issue. Obs.: **Caso a issue que você for resolver não tiver um responsável, torne-se ele**
 - # Labels

   - Utilize as labels para especificar se a issue deve ser feita no **backend** ou **frontend**
   - Toda issue **deve conter** a label **implementation** para informar que a implementação dela está sendo feita
   - Após implementar, adicione a label **test** para especificar que você está desenvolvendo os tests
   - Ao finalizar a issue, ela **deve conter** as labels: **backend** ou **frontend**, **implementation**, **test**, e em alguns casos **refactor**,
       caso seja necessário refatorar o código
