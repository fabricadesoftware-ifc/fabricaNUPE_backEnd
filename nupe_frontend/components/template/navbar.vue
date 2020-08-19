<template>
  <b-navbar :fixed-top="true" type="is-dark">
    <template slot="brand">
      <b-navbar-item>
        <sidebar />
      </b-navbar-item>
    </template>
    <template slot="start"></template>

    <template slot="end">
      <b-navbar-item>
        <nuxt-link to="/">Home</nuxt-link>
      </b-navbar-item>
      <b-navbar-item href="#">Documentation</b-navbar-item>
    </template>
  </b-navbar>
</template>

<script>
import sidebar from "@/components/template/sidebar.vue";
export default {
  components: {
    sidebar,
  },
};
</script>
