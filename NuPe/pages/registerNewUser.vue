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
      <div>
        <b-steps
          v-model="activeStep"
          :animated="isAnimated"
          :rounded="isRounded"
          :has-navigation="hasNavigation"
          :icon-prev="prevIcon"
          :icon-next="nextIcon"
          :label-position="labelPosition"
          :mobile-mode="mobileMode"
        >
          <b-step-item step="1" label="Informações Básica" :clickable="isStepsClickable">
            <h1 class="title has-text-centered">Informações Básica</h1>
            <person v-model="personForm" @updatePersonForm="updatePersonForm($event)" />
            <h1>{{personForm}}</h1>
          </b-step-item>

          <b-step-item step="2" label="Informações do Aluno" :clickable="isStepsClickable">
            <h1 class="title has-text-centered">Informações do Aluno</h1>
            <student />
          </b-step-item>

          <b-step-item
            v-if="!isUnderAge"
            step="3"
            label="Informações do Responsável"
            :clickable="isStepsClickable"
          >
            <h1 class="title has-text-centered">Informações do Responsável</h1>
          </b-step-item>

          <template v-if="customNavigation" slot="navigation" slot-scope="{previous, next}">
            <b-button
              outlined
              type="is-danger"
              icon-pack="fas"
              icon-left="backward"
              :disabled="previous.disabled"
              @click.prevent="previous.action"
            >Previous</b-button>
            <b-button
              outlined
              type="is-success"
              icon-pack="fas"
              icon-right="forward"
              :disabled="next.disabled"
              @click.prevent="next.action"
            >Next</b-button>
          </template>
        </b-steps>
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
      personForm: {
        age: "",
      },
      activeStep: 0,
      isUnderAge: false,

      isAnimated: true,
      isRounded: true,
      isStepsClickable: true,

      hasNavigation: true,
      customNavigation: false,

      prevIcon: "chevron-left",
      nextIcon: "chevron-right",
      labelPosition: "bottom",
      mobileMode: "minimalist",
    };
  },
  methods: {
    updatePersonForm(newPersonForm) {
      this.personForm = newPersonForm;

      var isUnderAge = newPersonForm.age < 18;
      this.setIsUnderAge(isUnderAge);
    },
    setIsUnderAge(newVal) {
      this.isUnderAge = newVal;
    },
  },
};
</script>

<style>
main {
  padding: 2% 5% 0% 5%;
}
</style>
