<template>
  <div>
    <div style="margin-left: 30px;">
      <a-button type="primary" :loading="loading" @click="hhh" style="margin-top: 15px">用例管理</a-button>
      <a-divider type="vertical" />
      <a-button type="primary" :loading="loading" style="margin-top: 15px">统计分析</a-button>
    </div>
    <div>
      <a-table
        :columns="columns"
        :rowKey="record => record.zxbh"
        :dataSource="data.reslist"
        :pagination="pagination"
        :loading="loading"
        @change="handleTableChange"
        style="margin-left: 30px;margin-right: 30px;"
      >
        <H3 slot="title">用例执行记录</H3>
        <span slot="action" slot-scope="record">
          <a-button type="primary" :loading="loading" @click="click_info(record.zxbh)">详情</a-button>
          <a-divider type="vertical" />
          <a-button type="primary" :loading="loading" @click="click_del(record.zxbh)">删除</a-button>
        </span>
      </a-table>
    </div>
  </div>
</template>
<script>
const columns = [
  {
    title: "名称",
    dataIndex: "ylmc",
    key: "ylmc",
    width: 400,
    align: "center"
  },
  {
    title: "执行时间",
    dataIndex: "zxsj",
    key: "zxsj",
    width: 400,
    align: "center"
  },
  {
    title: "覆盖率",
    key: "fgl",
    dataIndex: "fgl",
    width: 200,
    align: "center"
  },
  {
    title: "成功率",
    key: "cgl",
    dataIndex: "cgl",
    width: 200,
    align: "center"
  },
  {
    title: "通过率",
    key: "tgl",
    dataIndex: "tgl",
    width: 200,
    align: "center"
  },
  {
    title: "操作",
    key: "action",
    width: 300,
    scopedSlots: { customRender: "action" },
    align: "center"
  }
];

export default {
  mounted() {
    this.xmid = this.$route.params.xmid;
    this.fetch(1);
  },
  data() {
    return {
      data: [],
      xmid: "",
      pagination: {
        defaultPageSize: 10,
        total: null,
        showQuickJumper: true
      },
      loading: false,
      columns
    };
  },
  methods: {
    handleTableChange(pageNumber) {
      this.fetch(pageNumber.current);
    },
    fetch(pagenum) {
      this.loading = true;
      this.$http
        .get("http://localhost:8585/" + this.xmid + "/zx_list/" + pagenum)
        .then(function(response) {
          var time = {};
          for (time in response.body.reslist) {
            // console.log(response.body.reslist[time].zxsj)
            response.body.reslist[time].zxsj = this.getdate(
              response.body.reslist[time].zxsj
            );
          }
          this.data = response.body;
          this.pagination.total = response.body.maxsize;
          this.current = 1;
        });
      this.loading = false;
    },
    hhh() {
      alert("hhhhh");
    },
    click_info(key) {
      alert("infokey:" + key);
    },
    click_del(key) {
      alert("delkey:" + key);
    },
    getdate(time) {
      var date = new Date(time);
      var y = date.getFullYear();
      var m = date.getMonth() + 1;
      m = m < 10 ? "0" + m : m;
      var d = date.getDate();
      d = d < 10 ? "0" + d : d;
      var h = date.getHours();
      h = h < 10 ? "0" + h : h;
      var minute = date.getMinutes();
      var second = date.getSeconds();
      minute = minute < 10 ? "0" + minute : minute;
      second = second < 10 ? "0" + second : second;
      return (
        y + "-" + m + "-" + d + " " + "　" + h + ":" + minute + ":" + second
      );
    }
  }
};
</script>