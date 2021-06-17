<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12" :loading="loading">
            <template slot="progress">
              <v-progress-linear color="primary" height="10" indeterminate />
            </template>
            <v-toolbar dark color="primary">
              <v-toolbar-title>用户登陆</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  v-model="username"
                  prepend-icon="mdi-account"
                  name="username"
                  label="Username"
                  type="text"
                />
                <v-text-field
                  id="password"
                  v-model="password"
                  prepend-icon="mdi-lock"
                  name="password"
                  label="Password"
                  type="password"
                />
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn color="primary" @click="login"> 登录 </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
export default {
  name: 'Login',
  data: () => ({
    loading: false,
    username: '',
    password: '',
  }),
  methods: {
    login() {
      this.loading = true
      setTimeout(() => (this.loading = false), 8000)
      this.$http
        .post('auth', { username: this.username, password: this.password })
        .then((response) => {
          console.log(response.data.access_token)
          // TODO:用户状态信息的存储
          localStorage.setItem('JWT_TOKEN', response.data.access_token)
          this.$router.push({ path: '/index' })
        })
        .catch((error) => {
          console.log(error)
        })
        .finally(() => {
          this.loading = false
        })
    },
  },
}
</script>
