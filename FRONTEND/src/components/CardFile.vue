<template>
  <v-data-table
    :headers="headers"
    :items="desserts"
    :loading="loading"
    loading-text="Loading... Please wait"
    class="px-8 py-4 elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title class="headline">文件总览</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-responsive max-width="350">
          <v-text-field
            class="pa-4"
            v-model="newCaseName"
            dense
            clearable
            flat
            hide-details
            outlined
            label="请输入要添加的案例名"
            append-outer-icon="mdi-plus"
            @click:append-outer="addCase"
          />
        </v-responsive>
      </v-toolbar>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <UploaderButton :rawItem="item" />
    </template>
  </v-data-table>
</template>

<script>
import UploaderButton from './UploaderButton.vue'

export default {
  components: { UploaderButton },
  data: () => ({
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
      { text: '音频', value: 'audioCount' },
      { text: '视频', value: 'videoCount' },
      { text: '压缩包', value: 'zipCount' },
      { text: '其他文件', value: 'othersCount' },
      { text: '上传资料', value: 'actions', sortable: false },
    ],
  }),
  mounted: function () {
    this.getCaseInfo()
  },
  methods: {
    getCaseInfo() {
      setTimeout(() => (this.loading = false), 8000)
      this.loading = true
      this.$http
        .get('/case/caseinfo')
        .then((response) => {
          this.desserts = response.data
          console.log(response.data)
        })
        .catch((error) => {
          console.log(error.response.data.msg)
        })
        .finally(() => {
          this.loading = false
        })
    },
    addCase() {
      setTimeout(() => (this.loading = false), 8000)
      this.$http
        .post('/case/addCase', { caseName: this.newCaseName })
        .then((response) => {
          console.log(response.data)
          this.getCaseInfo()
          this.newCaseName = ''
        })
        .catch((error) => {
          // todo：封装一个全局的alert组件
          alert(error.response.data.msg)
        })
        .finally(() => {
          this.loading = false
        })
    },
  },
}
</script>

<style>
</style>