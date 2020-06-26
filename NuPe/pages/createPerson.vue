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
    },
    getListOfPeople(tokenUser) {
      this.$axios
        .get("/api/v1/person/", {
          headers: { Authorization: "Bearer ".concat(tokenUser) }
        })
        .then(resp => {
          console.log(resp.data);
        })
        .catch(err => {
          alert("Erro no metodo getListOfPeople");
          console.log(err);
        });
    },

    getPerson(tokenUser, cpf) {
      this.$axios
        .get("/api/v1/person/".concat(cpf, "/"), {
          headers: { Authorization: "Bearer ".concat(tokenUser) }
        })
        .then(resp => {
          console.log(resp.data);
        })
        .catch(err => {
          alert("Erro no metodo getPerson");
          console.log(err);
        });
    },
    deletePerson(tokenUser, cpf) {
      this.$axios
        .delete("/api/v1/person/".concat(cpf, "/"), {
          headers: { Authorization: "Bearer ".concat(tokenUser) }
        })
        .then(resp => {
          alert("Usuario DELETADO com sucesso");
          console.log(resp.data);
        })
        .catch(err => {
          alert("Erro no método deletePerson");
          console.log(err);
        });
    }
  },
  mounted() {
    this.getListOfPeople("0gKYHspvPjCvx8n2c90A0HIsqUIKXt");
  }
};
</script>
<style>
</style>