<template>
  <b-table :data="data" :columns="columns"></b-table>
</template>

<script>
export default {
  data() {
    return {
      data: [
        {
          cnpj: "10.635.424/0003-48",
          campus_name: "Araquari",
          institution_name: "IFC - Instituto Federal Catarinense",
          general_director: "Cleder Alexandre Somensi",
        },
        {
          cnpj: "10.635.424/0003-48",
          campus_name: "Araquari",
          institution_name: "IFC - Instituto Federal Catarinense",
          general_director: "Cleder Alexandre Somensi",
        },
        {
          cnpj: "10.635.424/0003-48",
          campus_name: "Araquari",
          institution_name: "IFC - Instituto Federal Catarinense",
          general_director: "Cleder Alexandre Somensi",
        },
        {
          cnpj: "10.635.424/0003-48",
          campus_name: "Araquari",
          institution_name: "IFC - Instituto Federal Catarinense",
          general_director: "Cleder Alexandre Somensi",
        },
        {
          cnpj: "10.635.424/0003-48",
          campus_name: "Araquari",
          institution_name: "IFC - Instituto Federal Catarinense",
          general_director: "Cleder Alexandre Somensi",
        },
      ],
      columns: [
        {
          field: "cnpj",
          label: "CNPJ",
          width: "40",
        },
        {
          field: "campus_name",
          label: "Campus",
        },
        {
          field: "institution_name",
          label: "Instituição",
        },
        {
          field: "general_director",
          label: "Diretor Geral",
        },
      ],
    };
  },
};
</script>

<style>
</style>