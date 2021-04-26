<template>
  <v-card class="pb-4 pt-1" rounded="lg">
    <v-card-title class="px-8 mx-6">
      <span class="headline">文件总览</span>
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
          this.newCaseName = ''
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

<style>
</style>