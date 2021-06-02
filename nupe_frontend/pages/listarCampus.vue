<template>
  <div>
    <title-bar :title-stack="titleStack" />

    <hero-bar>
      Gerenciamento de Campus
      <template v-slot:right>
        <router-link to="/" class="button"> Dashboard </router-link>
      </template>
    </hero-bar>
    <card-component
      class="has-table has-mobile-sort-spaced"
      title="Câmpus"
      icon="puzzle"
    >
      <listar-campus />
    </card-component>
  </div>
</template>

<script>
import HeroBar from "@/components/templates/HeroBar";
import TitleBar from "@/components/templates/TitleBar";
import CardComponent from "@/components/templates/CardComponent";

import ListarCampus from "@/components/campus/ListarCampus";

export default {
  auth: false,
  components: { ListarCampus, TitleBar, HeroBar, CardComponent },

  computed: {
    titleStack() {
      return ["Admin", "Listagem de Campus"];
    },
  },
};
</script>