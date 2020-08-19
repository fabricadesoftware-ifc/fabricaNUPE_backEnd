<template>
  <section>
    <b-sidebar :overlay="true" :right="true" :fullheight="true" type="is-dark" :open.sync="open">
      <div class="p-1"></div>
    </b-sidebar>

    <div @click="open = !open">
      <b-icon icon="view-dashboard" size="is-large" type="is-success"></b-icon>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      open: false,
    };
  },
};
</script>

<style scoped>
.p-1 {
  padding: 1em;
}
</style>