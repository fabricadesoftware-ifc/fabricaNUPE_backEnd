import LocalScheme from "@nuxtjs/auth/lib/schemes/local";

export default class CustomAuthScheme extends LocalScheme {
  async login(endpoint) {
    if (!this.options.endpoints.login) {
      return;
    }

    // Ditch any leftover local tokens before attempting to log in
    await this.$auth.reset();

    const token = btoa(
      `${this.options.client_id}:${this.options.client_secret}`
    );

    this.$auth.ctx.app.$axios.setHeader("Authorization", "Basic " + token);
    // this.$auth.ctx.app.$axios.config.withCredentials = true;
    // withCredentials: true
    // this.$auth.ctx.app.$axios.setHeader(
    //   "Content-Type",
    //   "application/x-www-form-urlencoded"
    // );

    const { response, result } = await this.$auth.request(
      endpoint,
      this.options.endpoints.login,
      true
    );

    if (this.options.tokenRequired) {
      const token = this.options.tokenType
        ? this.options.tokenType + " " + result
        : result;

      this.$auth.setToken(this.name, token);
      this._setToken(token);
    }

    if (this.options.autoFetchUser) {
      await this.fetchUser();
    }

    return response;
  }
}
