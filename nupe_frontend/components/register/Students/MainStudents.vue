<template>
  <div class="mySpace">
    <CreateStudents />
    <SelectStudent />
    <ListStudents :allStudents="allStudents" />
  </div>
</template>
<script>
import CreateStudents from "@/components/register/Students/CreateStudents.vue";
import ListStudents from "@/components/register/Students/ListStudents.vue";
import SelectStudent from "@/components/register/Students/SelectStudent.vue";
export default {
  components: {
    CreateStudents,
    ListStudents,
    SelectStudent,
  },
  data() {
    return {
      allStudents: [],
    };
  },
};
</script>
<style scoped>
.mySpace {
  margin: 2%;
}
</style>
