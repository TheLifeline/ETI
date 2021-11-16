<template>
  <v-dialog
    persistent
    v-model="dialog"
    max-width="600px"
    transition="dialog-top-transition"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn v-bind="attrs" v-on="on" icon>
        <v-icon>mdi-arrow-up-bold-box-outline</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">资料详情</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="12">
              <v-file-input
                chips
                show-size
                counter
                label="上传文件"
                v-model="file"
                @change="onChange()"
              ></v-file-input>
            </v-col>
            <v-col cols="12" sm="6" md="6">
              <v-text-field
                label="文件来源"
                required
                v-model="fileOrigin"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                :items="fileTypeItems"
                item-text="text"
                item-value="value"
                label="文件类型"
                v-model="fileType"
                required
              ></v-select>
            </v-col>
            <v-col cols="12" sm="12">
              <v-autocomplete
                :items="fileLableItems"
                label="文件标签"
                v-model="fileLable"
                chips
                small-chips
                multiple
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" md="12">
              <v-textarea
                solo
                v-model="describe"
                label="文件相关描述"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialog = false"> 关闭 </v-btn>
        <v-btn color="blue darken-1" text @click="upload">
          选择文件，开始上传
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ['rawItem'],
  data() {
    return {
      dialog: false,
      file: null,
      describe: '',
      fileOrigin: '',
      fileType: '',
      fileTypeItems: [
        { text: '图片', value: 'image' },
        { text: '文本', value: 'text' },
        { text: '音频', value: 'audio' },
        { text: '视频', value: 'video' },
        { text: '压缩包', value: 'zip' },
        { text: '其他文件', value: 'others' },
      ],
      fileLable: '',
      fileLableItems: ['指纹', '结果文件', '中间镜像', '数据流文件'],
    }
  },
  mounted() {},
  computed: {},
  methods: {
    upload() {
      this.$uploader.opts.target = window.axiosBaseUrl.slice(5) + 'file/upload'
      this.$uploader.opts.allowDuplicateUploads = true
      const fileQuery = {
        caseID: this.rawItem.caseID,
        caseName: this.rawItem.caseName,
        describe: this.describe,
        fileOrigin: this.fileOrigin,
        fileType: this.fileType,
        fileLable: this.fileLable,
      }
      this.$uploader.opts.query = fileQuery
      this.$uploader.opts.initFileFn = function (file, query = fileQuery) {
        file.query = query
      }
      this.$uploader.addFile(this.file)
      this.$uploader.upload()
      this.file = null
      this.fileType = ''
      this.fileOrigin = ''
      this.fileLable = ''
      this.textarea = ''
      this.dialog = false
    },
    onChange() {
      if (this.file) {
        // todo
        this.$http
          .post('/file/test', {
            caseID: this.rawItem.caseID,
            caseName: this.rawItem.caseName,
            fileName: this.file.name,
          })
          .then((response) => {
            console.log(response.data)
          })
          .catch((error) => {
            alert(error.response.data.msg)
            this.file = null
          })
          .finally(() => {})
        // todo：添加一个自动填充类型的
        console.log(this.file)
      } else {
        this.fileType = ''
      }
    },
  },
  destroyed() {},
}
</script>

<style scoped lang="scss">
</style>