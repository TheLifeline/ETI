<template>
  <div id="global-uploader">
    <!-- 上传 -->
    <uploader
      ref="uploader"
      :options="options"
      :autoStart="true"
      @file-added="onFileAdded"
      @file-success="onFileSuccess"
      @file-progress="onFileProgress"
      @file-error="onFileError"
      class="uploader-app"
    >
      <uploader-unsupport></uploader-unsupport>

      <uploader-btn id="global-uploader-btn" ref="uploadBtn">选择文件</uploader-btn>

      <v-btn v-show="buttonShow" @click="fileListShow" class="uploader-btn">上传列表</v-btn>
      <uploader-list v-show="panelShow">
        <div
          class="file-panel"
          slot-scope="props"
          :class="{ collapse: collapse }"
        >
          <div class="file-title">
            <h2>文件列表</h2>
            <div class="operate">
              <v-btn
                @click="fileListShow"
                type="text"
                :title="collapse ? '展开' : '折叠'"
                >最小化
              </v-btn>
            </div>
          </div>

          <ul class="file-list" id="i-file-list">
            <li v-for="file in props.fileList" :key="file.id">
              <uploader-file
                :class="'file_' + file.id"
                ref="files"
                :file="file"
                :list="true"
              ></uploader-file>
            </li>
            <div class="no-file" v-if="!props.fileList.length">
              暂无待上传文件
            </div>
          </ul>
        </div>
      </uploader-list>
    </uploader>
  </div>
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

<style scoped lang="scss">
#global-uploader {
  position: fixed;
  z-index: 60;
  right: 15px;
  bottom: 15px;
  .uploader-app {
    width: 520px;
  }
  .uploader-btn{
    float: right;
  }
  .file-panel {
    background-color: #fff;
    border: 1px solid #e2e2e2;
    border-radius: 7px 7px 0 0;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    .file-title {
      display: flex;
      height: 40px;
      line-height: 40px;
      padding: 0 15px;
      border-bottom: 1px solid #ddd;
      .operate {
        flex: 1;
        text-align: right;
      }
    }
    .file-list {
      position: relative;
      height: 240px;
      overflow-x: hidden;
      overflow-y: auto;
      background-color: #fff;
      > li {
        background-color: #fff;
      }
    }
    &.collapse {
      .file-title {
        background-color: #e7ecf2;
      }
    }
  }
  .no-file {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 16px;
  }
}
/* 隐藏上传按钮 */
#global-uploader-btn {
  position: absolute;
  clip: rect(0, 0, 0, 0);
}
</style>