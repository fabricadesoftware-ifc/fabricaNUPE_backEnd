<template>
  <div>
    <CreateStudents />
    <SelectStudent />
    <ListStudents />
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
};
</script>