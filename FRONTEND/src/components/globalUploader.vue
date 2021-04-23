<template>
<v-container class="d-flex justify-end align-self-end mr-0 mt-auto mb-0 global-uploader" >
  <v-fab-transition>
    <v-btn v-show="buttonShow" @click="fileListShow" absolute bottom righ><v-icon>mdi-plus</v-icon></v-btn>
  </v-fab-transition>
  <v-card elevation="7" outlined v-show="panelShow" >
    <v-card-title class="justify-end">文件列表
      <v-card-actions>
        <v-btn small icon @click="fileListShow">
          <v-icon > mdi-minus </v-icon>
        </v-btn>
      </v-card-actions>
    </v-card-title>

    <v-card-text>
    <uploader
      ref="uploader"
      :options="options"
      :autoStart="true"
      @file-added="onFileAdded"
      @file-success="onFileSuccess"
      @file-progress="onFileProgress"
      @file-error="onFileError"
    >
      <uploader-unsupport></uploader-unsupport>

      <uploader-btn ref="uploadBtn">选择文件</uploader-btn>
      <uploader-list> </uploader-list>
    </uploader>
    </v-card-text>
  </v-card>
</v-container>
</template>

<script>
/**
 *   全局上传插件
 *   调用方法：Bus.$emit('openUploader', {}) 打开文件选择框，参数为需要传递的额外参数
 *   监听函数：Bus.$on('fileAdded', fn); 文件选择后的回调
 *            Bus.$on('fileSuccess', fn); 文件上传成功的回调
 */
import Bus from './bus'

export default {
  data() {
    return {
      options: {
        target: '//localhost:5000/upload',
        chunkSize: '2048000',
        fileParameterName: 'file',
        maxChunkRetries: 3,
        testChunks: false,
        headers: {
          // TODO: 这里需要添加相关的认证
          // Authorization: Ticket.get() && "Bearer " + Ticket.get().access_token
        },
        query() {},
      },
      panelShow: false, // 选择文件后，展示上传panel
      buttonShow: false,
      collapse: false,
    }
  },
  mounted() {
    Bus.$on('openUploader', (query) => {
      this.params = query || {}
      if (this.$refs.uploadBtn) {
        document.getElementById('global-uploader-btn').click()
      }
    })
  },
  computed: {
    // Uploader实例
    uploader() {
      return this.$refs.uploader.uploader
    },
  },
  methods: {
    onFileAdded(file) {
      this.panelShow = true
      Bus.$emit('fileAdded')
    },
    onFileProgress(rootFile, file, chunk) {
      console.log('上传中')
    },
    onFileSuccess(rootFile, file, response, chunk) {
      // let res = JSON.parse(response)
      // // 服务器自定义的错误（即虽返回200，但是是错误的情况），这种错误是Uploader无法拦截的
      // if (!res.result) {
      //   // 文件状态设为“失败”
      //   console.log('error')
      //   return
      // }
      Bus.$emit('fileSuccess')
      console.log('上传成功')
    },
    onFileError(rootFile, file, response, chunk) {
      console.log({
        message: response,
        type: 'error',
      })
    },
    fileListShow() {
      if (!this.panelShow) {
        this.collapse = true
      } else {
        this.collapse = false
      }
      this.panelShow = !this.panelShow
      this.buttonShow = !this.panelShow
    },
    close() {
      this.uploader.cancel()
      this.panelShow = false
      this.buttonShow = !this.panelShow
    },
  },
  watch: {},
  destroyed() {
    Bus.$off('openUploader')
  },
  components: {},
}
</script>

<style scoped>
.global-uploader{
  position: fixed;
  z-index: 60;
  right: 15px;
  bottom: 15px;
}
</style>