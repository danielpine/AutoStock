<template>
  <div style="height: 100%">
    <meta charset="UTF-8" />
    <el-table
      stripe
      border
      v-loading="proc_loading"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
      :data="
        process_list.filter(
          (data) =>
            !search ||
            JSON.stringify(data).toLowerCase().includes(search.toLowerCase())
        )
      "
      style="width: 100%"
      max-height="700"
      :default-sort="{ prop: 'MemUsed', order: 'descending' }"
      size="mini"
      tooltip-effect="dark"
    >
      <el-table-column type="index"> </el-table-column>
      <el-table-column prop="Pid" label="Pid" leba sortable width="180">
      </el-table-column>
      <el-table-column prop="Ppid" label="Ppid" leba sortable width="180">
      </el-table-column>
      <el-table-column prop="Name" label="Name" sortable width="180">
      </el-table-column>
      <el-table-column
        prop="MemUsed"
        label="MemUsed"
        width="180"
        :sort-method="sort_mem"
        sortable
      >
      </el-table-column>
      <el-table-column
        prop="Cpu_Percent"
        label="Cpu_Percent"
        width="180"
        :sort-method="sort_cpu"
        sortable
      >
      </el-table-column>
      <el-table-column
        prop="Cmdline"
        label="Cmdline"
        :show-overflow-tooltip="true"
      >
        <template slot="header" slot-scope="scope">
          <el-input
            v-model="search"
            size="mini"
            placeholder="输入关键字搜索"
            clearable
          />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
module.exports = {
  data: function () {
    return {
      search: "",
    };
  },
  mounted: function () {},
  created: function () {},
  methods: {
    sort_mem: function (a, b) {
      return parseFloat(a["MemUsed"]) - parseFloat(b["MemUsed"]);
    },
    sort_cpu: function (a, b) {
      return parseFloat(a["Cpu_Percent"]) - parseFloat(b["Cpu_Percent"]);
    },
    formatter_float(row, column) {
      return column;
    },
  },
  props: ["process_list", "proc_loading"],
};
</script>
<style>
.hello {
  background-color: #ffe;
}
</style>
