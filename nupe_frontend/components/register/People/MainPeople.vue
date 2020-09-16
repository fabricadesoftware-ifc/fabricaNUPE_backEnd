<template>
  <div class="mySpace">
    <CreatePeople />
    <SelectPerson />
    <ListPeople :allPeople="allPeople" />
  </div>
</template>
<script>
import CreatePeople from "@/components/register/People/CreatePeople.vue";
import ListPeople from "@/components/register/People/ListPeople.vue";
import SelectPerson from "@/components/register/People/SelectPerson.vue";
export default {
  components: {
    CreatePeople,
    ListPeople,
    SelectPerson,
  },
  data() {
    return {
      allPeople: [
        {
          id: 1,
          first_name: "teste 1",
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
        {
          id: 23,
          first_name: "teste 3",
          last_name: "filtro 3",
          cpf: "3333333333333",
          contact: "4444444444444",
          gender: "M",
          birthday_date: "02/02/0003",
        },
        {
          id: 4,
          first_name: "teste 4",
          last_name: "filtro 4",
          cpf: "4444444444",
          contact: "44444443333333333",
          gender: "M",
          birthday_date: "02/02/0004",
        },
        {
          id: 5,
          first_name: "teste 5",
          last_name: "filtro 5",
          cpf: "5555555555",
          contact: "5555555555555",
          gender: "F",
          birthday_date: "02/02/0002",
        },
        {
          id: 6,
          first_name: "teste 6",
          last_name: "filtro 6",
          cpf: "6666666666666666",
          contact: "6666666666666",
          gender: "F",
          birthday_date: "02/11/0002",
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