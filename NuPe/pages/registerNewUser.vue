<template>
  <div>
    <header>
      <navbar />
      <section class="hero is-dark">
        <div class="hero-body">
          <div class="container">
            <h1 class="title">Área de Cadastro</h1>
            <h2 class="subtitle">Registre Novos Users na API</h2>
          </div>
        </div>
      </section>
    </header>
    <main>
      <div class="columns">
        <div class="column">
          <b-button expanded @click="chooseForm = 'Student'" type="is-dark">Formulário Estudante</b-button>
        </div>
        <div class="column">
          <b-button expanded @click="chooseForm = 'Person'" type="is-dark">Formulário Pessoa</b-button>
        </div>
      </div>
      <div class="columns">
        <div class="column">
          <div v-if="chooseForm === 'Person'">
            <Person />
          </div>
          <div v-else-if="chooseForm === 'Student'">
            <Student />
          </div>
        </div>
      </div>
    </main>
    <footerBase />
  </div>
</template>
<script>
import navbar from "@/components/template/navbar.vue";
import footerBase from "@/components/template/footerBase.vue";
import Person from "@/components/register/Person.vue";
import Student from "@/components/register/Student.vue";
export default {
  components: {
    Person,
    Student,
    navbar,
    footerBase,
  },
  data() {
    return {
      chooseForm: "Person",
    };
  },
};
</script>

<style>
main {
  padding: 2% 5% 0% 5%;
}
</style>
