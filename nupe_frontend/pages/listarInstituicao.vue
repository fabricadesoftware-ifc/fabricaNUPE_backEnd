<template>
  <div>
    <title-bar :title-stack="titleStack" />

    <hero-bar>
      Listagem de Instituição
      <template v-slot:right>
        <router-link to="/" class="button"> Dashboard </router-link>
      </template>
    </hero-bar>
    <card-component
      class="has-table has-mobile-sort-spaced"
      title="Câmpus"
      icon="puzzle"
    >
      <listar-instituicao />
    </card-component>
  </div>
</template>

<script>
import HeroBar from "@/components/templates/HeroBar";
import TitleBar from "@/components/templates/TitleBar";
import CardComponent from "@/components/templates/CardComponent";

import ListarInstituicao from "@/components/instituicao/ListarInstituicao";

export default {
  auth: false,
  components: { ListarInstituicao, TitleBar, HeroBar, CardComponent },

  computed: {
    titleStack() {
      return ["Admin", "Listagem de Instituição"];
    },
  },
};
</script>