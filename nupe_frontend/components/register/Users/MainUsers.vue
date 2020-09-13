<template>
  <div class="box mySpace">
    <!--Formulario para usuarios-->
    <CreateUsers />
    <hr />
    <ListUsers :allUsers="allUsers" />
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
  data() {
    return {
      allUsers: [
        {
          id: 1,
          first_name: "teste",
          last_name: "filtro",
        },
        {
          id: 2,
          first_name: "teste 2",
          last_name: "filtro 2",
        },
      ],
    };
  },
};
</script>
<style scoped>
.mySpace {
  margin: 2%;
}
</style>