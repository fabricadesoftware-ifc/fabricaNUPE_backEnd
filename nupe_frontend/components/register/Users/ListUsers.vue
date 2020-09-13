<template>
  <div>
    <label class="title">TODOS OS USERS</label>
    <b-table :data="data" :columns="columns"></b-table>
  </div>
</template>
<script>
export default {
  data() {
    return {
      data: [
        {
          id: 1,
          first_name: "Jesse",
          last_name: "Simmons",
        },
        {
          id: 2,
          first_name: "John",
          last_name: "Jacobs",
        },
        {
          id: 3,
          first_name: "Tina",
          last_name: "Gilbert",
        },
        {
          id: 4,
          first_name: "Clarence",
          last_name: "Flores",
        },
        {
          id: 5,
          first_name: "Anne",
          last_name: "Lee",
        },
      ],
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