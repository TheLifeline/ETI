<template>
  <v-card class="pb-4 pt-1" rounded="lg">
    <v-card-title class="px-8 mx-6">
      <span class="headline py-4">上传列表</span>
      <v-spacer></v-spacer>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="desserts"
      :loading="loading"
      loading-text="Loading... Please wait"
      class="px-6 mx-4"
    >
      <template v-slot:[`item.progressRain`]="{ item }">
        <v-progress-circular
          :value="desserts[item.fileID].progess"
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
  </v-card>
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
          progess: 0,
          fileName: this.$uploader.files[i].name,
          caseName: this.$uploader.files[i].uploader.opts.query.caseName,
          fileOrigin: this.$uploader.files[i].uploader.opts.query.fileOrigin,
          fileSize: this.$uploader.files[i].size,
          timeRemaining: this.$uploader.files[i].timeRemaining(),
          completed: this.$uploader.files[i].isComplete(),
          ispaused: this.$uploader.files[i].paused,
          iserror: this.$uploader.files[i].error,
        })
      }
      this.interval = setInterval(() => {
        for (let i = 0; i < this.desserts.length; i++) {
          const fileID = this.desserts[i].fileID
          const itemFile = this.$uploader.files[fileID]
          this.desserts[i].completed = itemFile.isComplete()
          if (!this.desserts[i].completed) {
            this.desserts[i].progess = 100
          }
          this.desserts[i].timeRemaining = itemFile.timeRemaining()
          this.desserts[i].ispaused = itemFile.paused
          this.desserts[i].iserror = itemFile.error
          if (this.desserts[i].iserror) {
            this.desserts[i].completed = 'Error'
            this.desserts[i].progess = 100
          }
        }
      }, 500)
      this.loading = false
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
        this.$uploader.files[item.fileID].cancel()
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