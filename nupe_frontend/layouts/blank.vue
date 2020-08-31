<template>
  <div>
    <aside-menu />
    <Nuxt />
  </div>
</template>

<script>
import AsideMenu from "@/components/templates/AsideMenu";
import { mapActions } from "vuex";

export default {
  components: { AsideMenu },
  created() {
    this.noAsideVisible();
  },
  methods: {
    ...mapActions("ui", ["noAsideVisible"])
  }
};
</script>

<style></style>
