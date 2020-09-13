<template>
  <section>
    <b-field label="Primeiro Nome">
      <b-input></b-input>
    </b-field>
    <b-field label="Ultimo Nome">
      <b-input></b-input>
    </b-field>
    <b-field label="CPF">
      <b-input></b-input>
    </b-field>
    <b-field label="Aniversário">
      <b-input></b-input>
    </b-field>
    <b-field label="Gênero">
      <b-input></b-input>
    </b-field>
    <b-field label="Contato">
      <b-input></b-input>
    </b-field>
    <label class="label">Foto de Perfil</label>
    <b-field class="file is-primary" :class="{'has-name': !!file}">
      <b-upload v-model="file" class="file-label">
        <span class="file-cta">
          <b-icon class="file-icon" icon="upload"></b-icon>
          <span class="file-label">FOTO DE PERFIL</span>
        </span>
        <span class="file-name" v-if="file">{{ file.name }}</span>
      </b-upload>
    </b-field>
  </section>
</template>
<script>
export default {
  data() {
    return {
      file: null,
    };
  },
};
</script>