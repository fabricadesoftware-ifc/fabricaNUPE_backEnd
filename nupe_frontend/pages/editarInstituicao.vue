<template>
  <div>
    <title-bar :title-stack="titleStack" />

    <hero-bar>
      Edição de Instituição
      <template v-slot:right>
        <router-link to="/" class="button"> Dashboard </router-link>
      </template>
    </hero-bar>
    <card-component
      class="has-table has-mobile-sort-spaced"
      title="Câmpus"
      icon="puzzle"
    >
      <editar-instituicao />
    </card-component>
  </div>
</template>

<script>
import HeroBar from "@/components/templates/HeroBar";
import TitleBar from "@/components/templates/TitleBar";
import CardComponent from "@/components/templates/CardComponent";

import EditarInstituicao from "@/components/instituicao/EditarInstituicao";

export default {
  auth: false,
  components: { EditarInstituicao, TitleBar, HeroBar, CardComponent },

  computed: {
    titleStack() {
      return ["Admin", "Edição de Instituição"];
    },
  },
};
</script>