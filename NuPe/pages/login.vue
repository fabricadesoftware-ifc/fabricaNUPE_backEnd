<template>
  <div class="margins">
    <div class="columns is-mobile">
      <div class="column">
        <div class="card box">
          <div class="card-content">
            <b-field>
              <b-input
                placeholder="Email"
                type="email"
                icon="email"
                icon-right="close-circle"
                icon-right-clickable
              ></b-input>
            </b-field>
            <b-field label="Password">
              <b-input type="password" password-reveal></b-input>
            </b-field>
            <b-button type="is-success" expanded>Entrar</b-button>
            <br />
            <b-button expanded>Esqueci minha senha</b-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.margins {
  padding: 10vh 10vw 10vh 10vw;
}
</style>