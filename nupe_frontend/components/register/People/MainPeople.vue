<template>
  <div class="box mySpace">
    <CreatePeople />
    <hr />
    <ListPeople :allPeople="allPeople" />
  </div>
</template>
<script>
import CreatePeople from "@/components/register/People/CreatePeople.vue";
import ListPeople from "@/components/register/People/ListPeople.vue";
export default {
  components: {
    CreatePeople,
    ListPeople,
  },
  data() {
    return {
      allPeople: [
        {
          id: 1,
          first_name: "teste",
          last_name: "filtro",
          cpf: "11111111111",
          contact: "121212121212",
          gender: "F",
          birthday_date: "01/01/0001",
        },
        {
          id: 2,
          first_name: "teste 2",
          last_name: "filtro 2",
          cpf: "2222222222",
          contact: "3333333333333333",
          gender: "M",
          birthday_date: "02/02/0002",
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