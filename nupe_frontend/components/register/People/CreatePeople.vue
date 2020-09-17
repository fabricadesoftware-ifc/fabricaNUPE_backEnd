<template>
  <div class="box">
    <label class="title">Criar Person</label>
    <b-field label-position="inside" label="Primeiro Nome">
      <b-input></b-input>
    </b-field>
    <b-field label-position="inside" label="Último Nome">
      <b-input></b-input>
    </b-field>
    <label class="label">Foto Do Aluno/a</label>
    <b-field class="file is-dark" :class="{'has-name': !!file}">
      <b-upload v-model="file" class="file-label">
        <span class="file-cta">
          <b-icon class="file-icon" icon="upload"></b-icon>
          <span class="file-label">Click to upload</span>
        </span>
        <span class="file-name" v-if="file">{{ file.name }}</span>
      </b-upload>
    </b-field>
    <b-field label-position="inside" label="CPF">
      <b-input></b-input>
    </b-field>
    <b-field label-position="inside" label="Data de Nascimento">
      <b-input></b-input>
    </b-field>
    <b-field llabel-position="inside" label="Gênero">
      <b-select>
        <option>F</option>
        <option>M</option>
      </b-select>
    </b-field>
    <b-field label-position="inside" label="Número de Telefone">
      <b-input placeholder="(ddd)nnnnn-nnnn"></b-input>
    </b-field>
    <b-button type="is-dark" expanded>CRIAR</b-button>
  </div>
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