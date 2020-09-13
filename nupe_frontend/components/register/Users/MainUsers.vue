<template>
  <div class="box mySpace">
    <!--Formulario para usuarios-->
    <CreateUsers />
    <hr />
    <ListUsers />
  </div>
</template>
<script>
import CreateUsers from "@/components/register/Users/CreateUsers.vue";
import ListUsers from "@/components/register/Users/ListUsers.vue";

export default {
  components: {
    CreateUsers,
    ListUsers,
  },
};
</script>
<style scoped>
.mySpace {
  margin: 2%;
}
</style>