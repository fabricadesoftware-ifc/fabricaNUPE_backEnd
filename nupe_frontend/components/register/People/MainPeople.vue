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
      allPeople: [],
    };
  },
};
</script>
<style scoped>
.mySpace {
  margin: 2%;
}
</style>