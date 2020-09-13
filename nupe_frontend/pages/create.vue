<template>
  <div class="space">
    <div class="buttons">
      <b-button type="is-dark" outlined>Outlined</b-button>
      <b-button type="is-dark" outlined>Outlined</b-button>
      <b-button type="is-dark" outlined>Outlined</b-button>
    </div>
    <CreatePerson />
  </div>
</template>
<script>
import CreatePerson from "@/components/templates/CreatePerson.vue";
export default {
  auth: false,
  components: {
    CreatePerson,
  },
};
</script>
<style>
.space {
  margin: 20px;
}
</style>