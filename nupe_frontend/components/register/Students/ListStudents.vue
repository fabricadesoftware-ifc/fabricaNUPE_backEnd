<template>
  <div>
    <label class="title">TODOS OS ESTUDANTES</label>
    <b-table :data="allStudents" :columns="columns" :sticky-header="true"></b-table>
  </div>
</template>
<script>
export default {
  props: {
    allStudents: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      columns: [
        {
          field: "registration",
          label: "REGISTRO",
          searchable: true,
        },
        {
          field: "person",
          label: "PERSON",
          searchable: true,
        },
        {
          field: "academic_education_institution_campus",
          label: "CAMPUS",
          searchable: true,
        },
        {
          field: "ingress_date",
          label: "DATA DE INGRESSO",
          searchable: true,
        },
      ],
    };
  },
};
</script>
