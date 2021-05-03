<template>
  <v-card class="pb-4 pt-1" rounded="lg">
    <v-card-title class="px-8 mx-6">
      <span class="headline">搜索结果</span>
      <v-spacer></v-spacer>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="desserts"
      :loading="loading"
      loading-text="Loading... Please wait"
      class="px-6 mx-4"
    >
      <template v-slot:[`item.actions`]>
        <UploaderButton />
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import UploaderButton from './UploaderButton.vue'

export default {
  components: { UploaderButton },
  data: () => ({
    loading: true,
    searchStr: '',
    desserts: [],
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
    this.searchStr = this.$route.query.searchStr
    this.getCaseInfo()
  },
  methods: {
    getCaseInfo() {
      setTimeout(() => (this.loading = false), 8000)
      this.loading = true
      this.$http
        .post('/file/search', { searchStr: this.searchStr })
        .then((response) => {
          console.log(response.data)
        })
        .catch((error) => {
          console.log(error.response.data.msg)
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