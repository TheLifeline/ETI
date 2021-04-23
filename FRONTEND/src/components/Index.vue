<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-container class="py-0 fill-height">
        <v-avatar class="mr-10" color="grey darken-1" size="40">
          <v-icon dark> mdi-account-circle </v-icon>
        </v-avatar>
        <v-toolbar-title>数据传输系统</v-toolbar-title>
        <v-spacer />

        <v-responsive max-width="660">
          <v-text-field
            v-model="searchStr"
            flat
            rounded
            solo-inverted
            label="输入文字以搜索"
            append-outer-icon="mdi-file-search"
            @click:append-outer="sendMessage"
          />
        </v-responsive>
      </v-container>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row align="center" justify="center">
          <v-col class="col-8">
            <v-card class="pb-4 pt-1">
              <v-card-title class="px-8 mx-6">
                文件总览
                <v-spacer></v-spacer>
                <v-text-field
                  class="col-4"
                  v-model="newCaseName"
                  dense
                  clearable
                  flat
                  solo-inverted
                  solo
                  label="请输入要添加的案例名"
                  append-outer-icon="mdi-plus"
                  @click:append-outer="addCase"
                />
              </v-card-title>
              <v-data-table
                :headers="headers"
                :items="desserts"
                :loading="loading"
                loading-text="Loading... Please wait"
                class="px-6 mx-4"
              >
                <template v-slot:[`item.actions`]>
                  <Uploader />
                </template>
              </v-data-table>
            </v-card>
            <!-- <v-sheet min-height="10vh" rounded="lg" class="pb-4 pt-1">
              <v-data-table
                :headers="headers"
                :items="desserts"
                class="elevation-0 pa-6 ma-4"
              >
                <template v-slot:[`item.actions`]>
                  <Uploader />
                </template>
              </v-data-table>
            </v-sheet> -->
          </v-col>
        </v-row>
      </v-container>
      <!-- <globalUploader /> -->
    </v-main>
  </v-app>
</template>

<script>
import Uploader from './Uploader.vue'

export default {
  components: { Uploader },
  data: () => ({
    searchStr: '',
    newCaseName: '',
    desserts: [],
    loading: true,
    headers: [
      {
        text: '案例名',
        align: 'start',
        sortable: false,
        value: 'caseName',
      },
      { text: '图片', value: 'imageCount' },
      { text: '文本', value: 'textCount' },
      { text: '表单', value: 'sheetCount' },
      { text: '镜像', value: 'mirrorCount' },
      { text: '压缩包', value: 'zipCount' },
      { text: '其他文件', value: 'othersCount' },
      { text: '上传资料', value: 'actions', sortable: false },
    ],
  }),
  mounted: function () {
    this.getCaseInfo()
  },
  methods: {
    sendMessage() {
      console.log('success')
      this.search_str = ''
    },
    getCaseInfo() {
      setTimeout(() => (this.loading = false), 8000)
      this.loading = true
      this.$http
        .get('caseinfo')
        .then((response) => {
          this.desserts = response.data
          console.log(response.data)
        })
        .catch((error) => {
          console.log(error)
        })
        .finally(() => {
          this.loading = false
        })
    },
    addCase() {
      setTimeout(() => (this.loading = false), 8000)
      this.$http
        .post('addCase', { caseNmae: this.newCaseName })
        .then((response) => {
          console.log(response.data)
          this.getCaseInfo()
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