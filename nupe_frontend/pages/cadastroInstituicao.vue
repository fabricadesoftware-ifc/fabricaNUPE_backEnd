<template>
  <div>
    <title-bar :title-stack="titleStack" />

    <hero-bar>
      Cadastro de instituição
      <template v-slot:right>
        <router-link to="/" class="button"> Dashboard </router-link>
      </template>
    </hero-bar>
    <card-component
      class="has-table has-mobile-sort-spaced"
      title="Câmpus"
      icon="puzzle"
    >
      <cadastro-instituicao/>
    </card-component>
  </div>
</template>

<script>
import HeroBar from "@/components/templates/HeroBar";
import TitleBar from "@/components/templates/TitleBar";
import CardComponent from "@/components/templates/CardComponent";

import CadastroInstituicao from "@/components/instituicao/CadastroInstituicao";

export default {
  auth: false,
  components: { CadastroInstituicao, TitleBar, HeroBar, CardComponent },

  computed: {
    titleStack() {
      return ["Admin", "Cadastro de Instituição"];
    },
  },
};
</script>