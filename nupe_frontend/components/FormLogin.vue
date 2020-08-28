<template>
  <card-component title="Acesso ao sistema" icon="lock">
    <form @submit.prevent="signin">
      <b-field label="Usuário">
        <b-input
          v-model="user.username"
          type="text"
          placeholder="Usuário"
          required
        >
        </b-input>
      </b-field>

      <b-field label="Senha">
        <b-input
          v-model="user.password"
          type="password"
          password-reveal
          placeholder="Senha"
          required
        >
        </b-input>
      </b-field>

      <b-field horizontal>
        <b-field grouped>
          <div class="control">
            <b-button native-type="submit" class="is-primary">Login</b-button>
          </div>
          <div class="control">
            <b-button type="is-primary is-outlined" @click="reset">
              Cancelar
            </b-button>
          </div>
        </b-field>
      </b-field>
    </form>
  </card-component>
</template>

<script>
import CardComponent from "@/components/templates/CardComponent";

export default {
  components: { CardComponent },
  data() {
    return {
      user: {
        grant_type: "password"
      }
    };
  },
  methods: {
    reset() {
      this.user = {
        grant_type: "password"
      };
    },
    async signin() {
      try {
        await this.$auth.loginWith("customStrategy", {
          data: this.user
        });
        this.$router.push("/");
      } catch (err) {
        for (const item in err.response.data) {
          this.$toast.error(item + ": " + err.response.data[item]);
        }
      }
    }
  }
};
</script>

<style></style>
