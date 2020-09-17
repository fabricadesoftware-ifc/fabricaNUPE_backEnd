<template>
  <div>
    <label class="title">TODOS OS USERS</label>
    <b-table :data="allUsers" :columns="columns" :sticky-header="true"></b-table>
  </div>
</template>
<script>
export default {
  props: {
    allUsers: {
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