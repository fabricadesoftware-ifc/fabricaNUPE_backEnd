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
      newStudent: {
        /*
          everything must be filled in correctly to avoid mistakes
        */

        registration: "",
        person: 0,
        academic_education_campus: 0,
        responsibles_persons: [0],
        ingress_date: ""
      }
    };
  },
  methods: {
    createNewPerson(tokenUser) {
      this.$axios
        .post("/api/v1/student/", this.newStudent, {
          headers: { Authorization: "Bearer ".concat(tokenUser) }
        })
        .then(resp => {
          console.log(resp.data);
          alert("Usuario criado com sucesso");
        })
        .catch(err => {
          console.log(err.data);
          alert("Erro ao criar usuario");
        });
    },
    getListOfStudents(tokenUser) {
      this.$axios
        .get("/api/v1/student/", {
          headers: { Authorization: "Bearer ".concat(tokenUser) }
        })
        .then(resp => {
          console.log(resp.data);
        })
        .catch(err => {
          console.log(err);
          alert("Erro na função getListOfStudent");
        });
    },
    getStudent(tokenUser, registration) {
      this.$axios
        .get("/api/v1/student/".concat(registration, "/"), {
          headers: { Authorization: "Bearer ".concat(tokenUser) }
        })
        .then(resp => {
          console.log(resp.data);
        })
        .catch(err => {
          console.log(err);
          alert("Erro na função getListOfStudent");
        });
    },
    deleteStudent(tokenUser, registration) {
      this.$axios
        .delete("/api/v1/person/".concat(registration, "/"), {
          headers: { Authorization: "Bearer ".concat(tokenUser) }
        })
        .then(resp => {
          alert("Student DELETADO com sucesso");
          console.log(resp.data);
        })
        .catch(err => {
          alert("Erro no método deleteStudent");
          console.log(err);
        });
    }
  },
  mounted() {
    this.getListOfStudents("TNtEgeHkjn7MHP4U92Jk9nzjUNptRt");
  }
};
</script>
<style>
</style>