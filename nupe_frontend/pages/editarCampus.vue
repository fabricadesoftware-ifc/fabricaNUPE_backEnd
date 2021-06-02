<template>
  <div>
    <title-bar :title-stack="titleStack" />

    <hero-bar>
      Edição de Campus
      <template v-slot:right>
        <router-link to="/" class="button"> Dashboard </router-link>
      </template>
    </hero-bar>
    <card-component
      class="has-table has-mobile-sort-spaced"
      title="Câmpus"
      icon="puzzle"
    >
      <editar-campus :valor="valor"/>
    </card-component>
  </div>
</template>

<script>
import HeroBar from "@/components/templates/HeroBar";
import TitleBar from "@/components/templates/TitleBar";
import CardComponent from "@/components/templates/CardComponent";

import EditarCampus from "@/components/campus/EditarCampus";

export default {
  auth: false,
  components: { EditarCampus, TitleBar, HeroBar, CardComponent },
  data(){
    return{
      valor:{
        nome:"Araquari",cnpj:"11.111.111.11",
      }
    }
  },
  computed: {
    titleStack() {
      return ["Admin", "Edição de Campus"];
    },
  },
};
</script>