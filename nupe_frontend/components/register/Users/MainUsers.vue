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
      allUsers: [
        {
          id: 1,
          first_name: "teste 1",
          last_name: "filtro 1",
        },
        {
          id: 2,
          first_name: "teste 2",
          last_name: "filtro 2",
        },
        {
          id: 3,
          first_name: "teste 3",
          last_name: "filtro 3",
        },
        {
          id: 4,
          first_name: "teste 4",
          last_name: "filtro 4",
        },
        {
          id: 5,
          first_name: "teste 5",
          last_name: "filtro 5",
        },
        {
          id: 6,
          first_name: "teste 6",
          last_name: "filtro 6",
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