<template>
  <v-data-table
    v-model="selected"
    :headers="dessertHeaders"
    :items="desserts"
    :loading="loading"
    loading-text="Loading... Please wait"
    :single-expand="true"
    show-expand
    show-select
    :single-select="false"
    class="px-8 py-4 elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title class="headline">搜索结果</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-btn @click="download"> 下载 </v-btn>
      </v-toolbar>
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">文件相关描述: {{ item.fileDescribe }}</td>
    </template>
  </v-data-table>
</template>

<script>
import Bus from './Bus'
export default {
  data: () => ({
    loading: false,
    selected: [],
    desserts: [],
    dessertHeaders: [
      {
        text: '文件名',
        align: 'start',
        sortable: false,
        value: 'fileName',
      },
      { text: '所属案例', value: 'caseName' },
      { text: '文件类型', value: 'fileType' },
      { text: '文件来源', value: 'fileOrigin' },
      { text: '文件标签', value: 'fileLable' },
      { text: '', value: 'data-table-expand' },
    ],
  }),
  mounted: function () {
    Bus.$on('mysearch', (val) => {
      this.getSearch(val)
    })
  },
  beforeDestroy: function () {
    Bus.$off('mysearch')
  },
  methods: {
    download() {
      for (let i = 0; i < this.selected.length; i++) {
        const item = this.selected[i]
        console.log('/file/download/' + item.caseID + '/' + item.fileName)
        this.$http
          .get('/file/download/' + item.caseID + '/' + item.fileName)
          .then((response) => {
            console.log(response)
            this.convertRes2Blob(response, item.fileName)
          })
          .catch((error) => {
            console.log(error.response.data.msg)
          })
      }
    },
    convertRes2Blob(response, fileName) {
      // 将二进制流转为blob
      const blob = new Blob([response.data], {
        type: 'application/octet-stream',
      })
      if (typeof window.navigator.msSaveBlob !== 'undefined') {
        // 兼容IE，window.navigator.msSaveBlob：以本地方式保存文件
        window.navigator.msSaveBlob(blob, decodeURI(fileName))
      } else {
        // 创建新的URL并指向File对象或者Blob对象的地址
        const blobURL = window.URL.createObjectURL(blob)
        // 创建a标签，用于跳转至下载链接
        const tempLink = document.createElement('a')
        tempLink.style.display = 'none'
        tempLink.href = blobURL
        tempLink.setAttribute('download', decodeURI(fileName))
        // 兼容：某些浏览器不支持HTML5的download属性
        if (typeof tempLink.download === 'undefined') {
          tempLink.setAttribute('target', '_blank')
        }
        // 挂载a标签
        document.body.appendChild(tempLink)
        tempLink.click()
        document.body.removeChild(tempLink)
        // 释放blob URL地址
        window.URL.revokeObjectURL(blobURL)
      }
    },
    getSearch(searchStr) {
      console.log(searchStr)
      this.loading = true
      this.$http
        .post('/file/search', { searchStr: searchStr })
        .then((response) => {
          this.desserts = response.data.json_list
        })
        .catch((error) => {
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