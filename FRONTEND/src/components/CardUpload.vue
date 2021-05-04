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
          <v-toolbar-title class="headline">上传列表</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
        </v-toolbar>
      </template>
      <template v-slot:[`item.progressRain`]="{ item }">
        <v-progress-circular
          :value="item.progess * 100"
          :size="25"
          :width="5"
          :color="
            item.iserror
              ? 'red accent-4'
              : item.completed
              ? 'green lighten-2'
              : 'grey'
          "
        ></v-progress-circular>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon
          class="mr-2"
          @click="pause(item)"
          v-show="!item.completed & !item.iserror"
        >
          {{ item.ispaused ? 'mdi-play' : 'mdi-pause' }}
        </v-icon>
        <v-icon @click="restart(item)">
          {{
            item.iserror
              ? 'mdi-restart'
              : item.completed
              ? 'mdi-check-bold'
              : ''
          }}
        </v-icon>
        <v-icon @click="cancel(item)">
          {{ item.completed ? '' : 'mdi-cancel' }}
        </v-icon>
      </template>
    </v-data-table>
</template>

<script>
export default {
  data: () => ({
    interval: {},
    desserts: [],
    loading: true,
    headers: [
      {
        text: '进度',
        align: 'start',
        sortable: false,
        value: 'progressRain',
      },
      { text: '文件名', value: 'fileName', sortable: false },
      { text: '所属案例', value: 'caseName', sortable: false },
      { text: '文件来源', value: 'fileOrigin', sortable: false },
      { text: '文件大小', value: 'fileSize' },
      { text: '是否完成', value: 'completed' },
      { text: '剩余时间', value: 'timeRemaining' },
      { text: '', value: 'actions', sortable: false },
    ],
  }),
  mounted: function () {
    this.getCaseInfo()
  },
  methods: {
    getCaseInfo() {
      setTimeout(() => (this.loading = false), 8000)
      this.loading = true
      for (let i = 0; i < this.$uploader.files.length; i++) {
        this.desserts.push({
          fileID: i,
          itemFile: this.$uploader.files[i],
          fileName: this.$uploader.files[i].name,
          fileSize: this.$uploader.files[i].size,
          caseName: this.$uploader.files[i].query.caseName,
          fileOrigin: this.$uploader.files[i].query.fileOrigin,
          timeRemaining: this.$uploader.files[i].timeRemaining(),
          completed: this.$uploader.files[i].isComplete(),
          progess: this.$uploader.files[i].progress(),
          ispaused: this.$uploader.files[i].paused,
          iserror: this.$uploader.files[i].error,
        })
      }
      this.resetFileInterval()
      this.loading = false
    },
    resetFileInterval() {
      clearInterval(this.interval)
      this.interval = setInterval(() => {
        this.desserts.forEach(function (item, index) {
          const itemFile = item.itemFile
          item.fileName = itemFile.name
          item.caseName = itemFile.query.caseName
          item.fileOrigin = itemFile.query.fileOrigin
          item.fileSize = itemFile.size
          item.completed = itemFile.isComplete()
          item.progess = itemFile.progress()
          item.timeRemaining = itemFile.timeRemaining()
          item.ispaused = itemFile.paused
          item.iserror = itemFile.error
          if (item.iserror) {
            item.completed = '错误'
          }
        })
      }, 500)
    },
    pause(item) {
      if (item.ispaused) {
        this.$uploader.files[item.fileID].resume()
      } else {
        this.$uploader.files[item.fileID].pause()
      }
      item.ispaused = this.$uploader.files[item.fileID].paused
    },
    restart(item) {
      if (item.iserror) {
        this.$uploader.files[item.fileID].retry()
      }
    },
    cancel(item) {
      if (!item.completed) {
        clearInterval(this.interval)
        this.desserts.splice(item.fileID, 1)
        item.itemFile.cancel()
        this.resetFileInterval()
      }
    },
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
}
</script>

<style>
</style>