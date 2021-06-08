<template>
  <div style="height: 100%;">
    <meta charset="UTF-8" />
    <div class="filter-container">
      <el-button
        style="margin-left: 10px;"
        type="primary"
        size="mini"
        icon="el-icon-edit"
        @click="handleCreate"
      >
        Add
      </el-button>
    </div>
    <br />
    <el-table
      stripe
      border
      v-loading="loading"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
      :data="
        tableData.filter(
          (data) =>
            !search ||
            JSON.stringify(data).toLowerCase().includes(search.toLowerCase()),
        )
      "
      style="width: 100%;"
      max-height="700"
      :default-sort="{ prop: 'MemUsed', order: 'descending' }"
      size="mini"
      tooltip-effect="dark"
    >
      <el-table-column type="index" label="#"></el-table-column>
      <el-table-column
        prop="id"
        label="ID"
        leba
        sortable
        width="80"
      ></el-table-column>
      <el-table-column
        prop="stock_id"
        label="股票代码"
        leba
        sortable
        width="105"
      ></el-table-column>
      <el-table-column
        label="监控阈值"
        prop="threshold_value"
        sortable
        width="105"
      ></el-table-column>
      <el-table-column
        label="阈值类型"
        prop="threshold_type"
        width="105"
        sortable
      ></el-table-column>
      <el-table-column
        label="监控类型"
        prop="monitoring_type"
        width="105"
        sortable
      ></el-table-column>
      <el-table-column
        label="压制次数"
        prop="over_limit"
        width="105"
        sortable
      ></el-table-column>
      <el-table-column
        label="达到次数"
        prop="over_count"
        width="105"
        sortable
      ></el-table-column>
      <el-table-column
        label="监控状态"
        prop="status"
        width="105"
        sortable
      ></el-table-column>
      <el-table-column prop="time_stamp" width="200">
        <template slot="header">
          <el-input
            v-model="search"
            size="mini"
            placeholder="输入关键字搜索"
            clearable
          />
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="right"
        label-width="70px"
        style="width: 400px; margin-left: 50px;"
      >
        <el-form-item label="股票代码" prop="stock_id">
          <el-input v-model="temp.stock_id" />
        </el-form-item>
        <el-form-item label="监控阈值" prop="threshold_value">
          <el-input v-model.number="temp.threshold_value">
            <template v-if="temp.threshold_type === 'percent'" slot="append">
              %
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="阈值类型" prop="threshold_type">
          <el-select
            v-model="temp.threshold_type"
            class="filter-item"
            placeholder="Please select"
          >
            <el-option label="绝对值" value="absolute"></el-option>
            <el-option label="百分比" value="percent"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="监控类型" prop="monitoring_type">
          <el-select
            v-model="temp.monitoring_type"
            class="filter-item"
            placeholder="Please select"
          >
            <el-option label="高于" value="high"></el-option>
            <el-option label="低于" value="low"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="压制次数" prop="over_limit">
          <el-input-number
            style="width: 100%;"
            v-model="temp.over_limit"
            :min="1"
            :max="5"
            title="检查符合多少次后触发通知"
          ></el-input-number>
        </el-form-item>
      </el-form>
      <!-- <pre>{{ temp }}</pre> -->
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
        >
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
module.exports = {
  data: function () {
    return {
      search: '',
      loading: false,
      tableData: [],
      dialogFormVisible: false,
      dialogStatus: 'create',
      temp: {
        id: undefined,
        stock_id: 'sz000069',
        threshold_value: '2.78',
        threshold_type: 'percent',
        status: '0',
        user_id: 'default',
        over_limit: 1,
        monitoring_type: 'high',
      },
      textMap: {
        update: 'Edit',
        create: 'Create',
      },
      rules: {
        type: [
          { required: true, message: 'type is required', trigger: 'change' },
        ],
        timestamp: [
          {
            type: 'date',
            required: true,
            message: 'timestamp is required',
            trigger: 'change',
          },
        ],
        title: [
          { required: true, message: 'title is required', trigger: 'blur' },
        ],
      },
      statusOptions: ['published', 'draft', 'deleted'],
    }
  },
  mounted: function () {},
  created: function () {
    this.loadTableData()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: undefined,
        stock_id: 'sz000068',
        threshold_value: '2.73',
        threshold_type: 'absolute',
        status: '0',
        user_id: 'default',
        over_limit: 1,
        monitoring_type: 'high',
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    loadTableData() {
      let that = this
      axios
        .get('/user/list')
        .then(function (res) {
          console.log(res)
          that.tableData = res.data
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          let that = this
          axios
            .post('/user/add', this.temp)
            .then(function (res) {
              console.log(res)
              if (res.data.success) {
                that.loadTableData()
                that.$notify({
                  title: 'Success',
                  message: 'Created Successfully',
                  type: 'success',
                  duration: 2000,
                })
              } else {
                that.$notify({
                  title: 'Failed',
                  message: 'Created Failed : ' + res.data.message,
                  type: 'error',
                  duration: 2000,
                })
              }
              that.dialogFormVisible = false
            })
            .catch(function (error) {
              console.log(error)
            })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateArticle(tempData).then(() => {
            const index = this.list.findIndex((v) => v.id === this.temp.id)
            this.list.splice(index, 1, this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000,
            })
          })
        }
      })
    },
    sort_mem: function (a, b) {
      return parseFloat(a['MemUsed']) - parseFloat(b['MemUsed'])
    },
    sort_cpu: function (a, b) {
      return parseFloat(a['Cpu_Percent']) - parseFloat(b['Cpu_Percent'])
    },
    formatter_float(row, column) {
      return column
    },
  },
  // props: ['tableData', 'loading']
}
</script>
<style>
.filter-item {
  width: 100%;
  display: inline-block;
  vertical-align: middle;
  margin-bottom: 10px;
}
</style>
