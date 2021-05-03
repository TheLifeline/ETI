<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-container class="py-0 fill-height">
        <v-avatar class="mr-5" color="grey darken-1" size="40">
          <v-icon dark>mdi-arrow-up-down-bold</v-icon>
        </v-avatar>
        <v-toolbar-title>数据传输系统</v-toolbar-title>

        <v-btn class="ml-10" text to="/index/file">文件总览</v-btn>
        <v-btn class="ml-5" text to="/index/upload">上传列表</v-btn>
        <v-btn class="ml-5" text to="/index/download">下载列表</v-btn>

        <v-spacer />

        <v-responsive max-width="660">
          <v-text-field
            v-model="searchStr"
            clearable
            flat
            hide-details
            rounded
            solo-inverted
            label="输入文字以搜索"
            append-outer-icon="mdi-file-search"
            @click:append-outer="searchFile"
          />
        </v-responsive>
      </v-container>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row align="center" justify="center">
          <v-col class="col-10">
            <router-view />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    searchStr: '',
  }),
  mounted: function () {
    this.routerPath('/index/file')
  },
  methods: {
    searchFile() {
      this.routerPath('/index/search', { searchStr: this.searchStr })
    },
    routerPath(path, query) {
      if (this.$route.path !== path) {
        this.$router.push({ path: path, query: query })
      }
    },
  },
}
</script>