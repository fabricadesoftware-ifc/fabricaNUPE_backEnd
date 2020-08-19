<template>
  <section>
    <h1>PESSOA</h1>
    <b-field>
      <b-input placeholder="Email" type="email"></b-input>
    </b-field>

    <b-field>
      <b-input name="age" v-model="form.age" placeholder="age" type="number" min="0" max="150"></b-input>
    </b-field>

    <b-field>
      <b-input
        placeholder="User handle (custom validation for only lowercase)"
        type="text"
        required
        validation-message="Only lowercase is allowed"
        pattern="[a-z]*"
      ></b-input>
    </b-field>

    <b-field>
      <b-input placeholder="URL" type="url"></b-input>
    </b-field>

    <b-field>
      <b-input
        type="textarea"
        minlength="10"
        maxlength="100"
        placeholder="Maxlength automatically counts characters"
      ></b-input>
    </b-field>
  </section>
</template>
<script>
export default {
  data() {
    return {
      form: {
        age: "",
      },
    };
  },
  watch: {
    form: {
      handler: function (newForm, oldForm) {
        this.$emit("updatePersonForm", newForm);
      },
      deep: true,
    },
  },
};
</script>
