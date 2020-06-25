<template>
  <div>
    <h1 class="title">CRIAR TELA DE CRIAÇÃO DE USUARIOS</h1>
    <h2 class="subtitle">INFORMAÇÕES UTEIS NO CONSOLE</h2>
  </div>
</template>
<script>
export default {
  data() {
    return {
      newPerson: {
        /*
          everything must be filled in correctly to avoid mistakes
        */

        first_name: "",
        last_name: "",
        cpf: "",
        birthday_date: "",
        gender: "",
        contact: ""
      }
    };
  },
  methods: {
    //don't forget the token, ex: createNewPerson("432mytoken1234")
    createNewPerson(tokenUser) {
      this.$axios
        .post("/api/v1/person/", this.newPerson, {
          headers: { Authorization: "Bearer ".concat(tokenUser) }
        })
        .then(resp => {
          console.log(resp.data);
          alert("Usuario criado com sucesso");
        })
        .catch(err => {
          console.log(err.data);
          alert("Erro ao criar usuario person");
        });
    }
  }
};
</script>
<style>
</style>