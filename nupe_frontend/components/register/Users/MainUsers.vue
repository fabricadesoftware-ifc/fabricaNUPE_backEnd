<template>
  <div class="mySpace">
    <!--Formulario para usuarios-->
    <CreateUsers />

    <SelectUser />

    <hr />

    <ListUsers :allUsers="allUsers" />
  </div>
</template>
<script>
import CreateUsers from "@/components/register/Users/CreateUsers.vue";
import ListUsers from "@/components/register/Users/ListUsers.vue";
import SelectUser from "@/components/register/Users/SelectUser.vue";

export default {
  components: {
    CreateUsers,
    ListUsers,
    SelectUser,
  },
  data() {
    return {
      allUsers: [],
    };
  },
};
</script>
<style scoped>
.mySpace {
  margin: 2%;
}
</style>