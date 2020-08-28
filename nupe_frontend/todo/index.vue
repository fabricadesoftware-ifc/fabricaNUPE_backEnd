<template>
  <div>
    <header>
      <navbar />
    </header>
    <main>
      <h1 class="title">Projeto NuPe</h1>
    </main>
    <footerBase />
  </div>
</template>
<script>
import navbar from "@/components/template/navbar.vue";
import footerBase from "@/components/template/footerBase.vue";
export default {
  components: {
    navbar,
    footerBase
  }
};
</script>
<style></style>
