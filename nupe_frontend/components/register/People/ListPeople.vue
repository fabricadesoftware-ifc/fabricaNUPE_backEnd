<template>
  <div>
    <label class="title">Todas as Person</label>
    <b-table :data="allPeople" :columns="columns" :sticky-header="true"></b-table>
  </div>
</template>
<script>
export default {
  props: {
    allPeople: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      columns: [
        {
          field: "first_name",
          label: "First Name",
          searchable: true,
        },
        {
          field: "last_name",
          label: "Last Name",
          searchable: true,
        },
        {
          field: "cpf",
          label: "CPF",
          searchable: true,
        },
        {
          field: "birthday_date",
          label: "Data de Aniversario",
          searchable: true,
        },
        {
          field: "gender",
          label: "Genero",
          searchable: true,
        },
        {
          field: "contact",
          label: "Número",
          searchable: true,
        },
        {
          field: "id",
          label: "ID",
          width: "100",
          numeric: true,
          searchable: true,
        },
      ],
    };
  },
};
</script>