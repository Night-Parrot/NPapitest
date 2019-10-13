<template>
  <div>
    <!-- 用例信息的抽屉 -->
    <div>
      <a-drawer
        title="用例管理"
        :placement="placement"
        :closable="true"
        @close="onClose"
        :visible="visible_ylgl"
        :destroyOnClose="true"
        height="800"
      >
        <div>
          <div style="margin-left: 30px;">
            <a-upload
              name="file"
              :multiple="true"
              action
              :headers="headers_upload"
              @change="handleChange"
            >
              <a-button type="primary" :loading="loading" style="margin-top: 15px">用例上传</a-button>
            </a-upload>
          </div>
          <a-table
            :columns="columns_yl"
            :rowKey="record => record.zxbh"
            :dataSource="data_yl"
            :pagination="pagination"
            :loading="loading"
            size="small"
            @change="handleTableChange_ylxx"
            style="margin-left: 30px;margin-right: 30px;margin-top: 15px"
          >
            <H3 slot="title">用例列表</H3>
            <span slot="action_yl" slot-scope="record">
              <a-button type="primary" :loading="loading" @click="click_info(record.ylmc)">执行</a-button>
              <a-divider type="vertical" />
              <a-button type="primary" :loading="loading" @click="click_del(record.scsj)">下载</a-button>
              <a-divider type="vertical" />
              <a-button type="primary" :loading="loading" @click="click_del(record.zxcs)">删除</a-button>
            </span>
          </a-table>
        </div>
      </a-drawer>
    </div>
    <!-- ============================================================================================================================== -->
    <!-- 统计分析的抽屉 -->

    <div>
      <a-drawer
        title="统计分析"
        :placement="placement"
        :closable="true"
        @close="onClose"
        :visible="visible_tjfx"
        :destroyOnClose="true"
        height="800"
      >
        <div>
          <H8>暂时没想好统计内容</H8>
          <H8>有想法请联系梁磊</H8>
        </div>
      </a-drawer>
    </div>
    <!-- ============================================================================================================================= -->
    <!-- 详情的抽屉 -->
    <div>
      <a-drawer
        title="执行情况"
        :placement="placement"
        :closable="true"
        @close="onClose"
        :visible="visible_zxinfo"
        :destroyOnClose="true"
        height="800"
      >
        <div>
          <div id="char_cgl" style="float: left;"></div>
          <div id="char_tgl" style="float: left;"></div>
        </div>
        <div>
          <a-table
            :columns="columns_zxinfo"
            :dataSource="data_zxinfo"
            class="components-table-demo-nested"
            :scroll="{y:550}"
            size="middle"
          >
            <a-table
              slot="expandedRowRender"
              :columns="innerColumns_zxinfo"
              :dataSource="innerData_zxinfo"
              :pagination="false"
              size="small"
              style="margin-left: 15px;margin-right: 15px"
            ></a-table>
          </a-table>
        </div>
      </a-drawer>
    </div>

    <!-- ============================================================================================================================= -->
    <div style="margin-left: 30px;">
      <a-button
        type="primary"
        :loading="loading"
        @click="showDrawer_ylgl"
        style="margin-top: 15px"
      >用例管理</a-button>
      <a-divider type="vertical" />
      <a-button
        type="primary"
        :loading="loading"
        style="margin-top: 15px"
        @click="showDrawer_tjfx"
      >统计分析</a-button>
    </div>
    <div>
      <a-table
        :columns="columns"
        :rowKey="record => record.zxbh"
        :dataSource="data.reslist"
        :pagination="pagination"
        :loading="loading"
        @change="handleTableChange_zxxx"
        style="margin-left: 30px;margin-right: 30px;"
      >
        <H3 slot="title">用例执行记录</H3>
        <span slot="action" slot-scope="record">
          <a-button type="primary" :loading="loading" @click="click_zxinfo(record.zxbh)">详情</a-button>
          <a-divider type="vertical" />
          <a-button type="primary" :loading="loading" @click="click_del(record.zxbh)">删除</a-button>
        </span>
      </a-table>
    </div>
  </div>
</template>
<script>
import G2 from "@antv/g2";
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
const columns_yl = [
  {
    title: "名称",
    dataIndex: "ylmc",
    key: "ylmc",
    width: 400,
    align: "center"
  },
  {
    title: "上传时间",
    dataIndex: "scsj",
    key: "scsj",
    width: 400,
    align: "center"
  },
  {
    title: "执行次数",
    dataIndex: "zxcs",
    key: "zxcs",
    width: 400,
    align: "center"
  },
  {
    title: "操作",
    key: "action_yl",
    width: 300,
    scopedSlots: { customRender: "action_yl" },
    align: "center"
  }
];

// =====成功率饼图的数据===================
var data_char_cgl = [
  {
    item: "事例一",
    count: 40,
    percent: 0.4
  },
  {
    item: "事例二",
    count: 21,
    percent: 0.21
  },
  {
    item: "事例三",
    count: 17,
    percent: 0.17
  },
  {
    item: "事例四",
    count: 13,
    percent: 0.13
  },
  {
    item: "事例五",
    count: 9,
    percent: 0.09
  }
];

// =================================
const columns_zxinfo = [
  {
    title: "名称",
    dataIndex: "name",
    key: "name",
    align: "center",
    width: 400
  },
  {
    title: "地址",
    dataIndex: "platform",
    key: "platform",
    align: "center",
    width: 300
  },
  {
    title: "响应时间",
    dataIndex: "version",
    key: "version",
    align: "center",
    width: 200
  },
  {
    title: "执行时间",
    dataIndex: "upgradeNum",
    key: "upgradeNum",
    align: "center",
    width: 100
  },
  {
    title: "接口状态",
    dataIndex: "creator",
    key: "creator",
    align: "center",
    width: 100
  },
  {
    title: "验证结果",
    dataIndex: "createdAt",
    key: "createdAt",
    align: "center",
    width: 200
  }
];

const data_zxinfo = [];
for (let i = 0; i < 10; ++i) {
  data_zxinfo.push({
    key: i,
    name: "Screem",
    platform: "iOS",
    version: "10.3.4.5654",
    upgradeNum: 500,
    creator: "Jack",
    createdAt: "2014-12-24 23:12:00"
  });
}

const innerColumns_zxinfo = [
  {
    title: "参数",
    dataIndex: "date",
    key: "date",
    align: "center",
    width: 400
  },
  {
    title: "预期返回值",
    dataIndex: "name",
    key: "name",
    align: "center",
    width: 400
  },
  {
    title: "实际返回值",
    dataIndex: "upgradeNum",
    key: "upgradeNum",
    align: "center",
    width: 400
  }
];

const innerData_zxinfo = [
  {
    key: 1,
    date: "2014-12-24 23:12:00",
    name: "This is production name",
    upgradeNum: "Upgraded: 56"
  }
];

// =================================

export default {
  mounted() {
    this.xmid = "testurl2";
    this.fetch(1);
  },
  data() {
    return {
      data_char_cgl: data_char_cgl,
      columns_zxinfo: columns_zxinfo,
      innerColumns_zxinfo: innerColumns_zxinfo,
      data_zxinfo: data_zxinfo,
      innerData_zxinfo: innerData_zxinfo,
      data: [],
      columns_yl: columns_yl,
      columns: columns,
      visible_zxinfo: false,
      data_yl: [
        {
          ylmc: "T3EV1.1-流程用例",
          scsj: "2019-10-13 20:50:32",
          zxcs: 55
        },
        {
          ylmc: "T3EV1.1-流程用例",
          scsj: "2019-10-13 20:50:32",
          zxcs: 55
        },
        {
          ylmc: "T3EV1.1-流程用例",
          scsj: "2019-10-13 20:50:32",
          zxcs: 55
        },
        {
          ylmc: "T3EV1.1-流程用例",
          scsj: "2019-10-13 20:50:32",
          zxcs: 55
        },
        {
          ylmc: "T3EV1.1-流程用例",
          scsj: "2019-10-13 20:50:32",
          zxcs: 55
        },
        {
          ylmc: "T3EV1.1-流程用例",
          scsj: "2019-10-13 20:50:32",
          zxcs: 55
        },
        {
          ylmc: "T3EV1.1-流程用例",
          scsj: "2019-10-13 20:50:32",
          zxcs: 55
        },
        {
          ylmc: "T3EV1.1-流程用例",
          scsj: "2019-10-13 20:50:32",
          zxcs: 55
        }
      ],
      xmid: "",
      visible_ylgl: false,
      visible_tjfx: false,
      fileList: [],
      headers_upload: "authorization-text",
      placement: "top",
      pagination: {
        defaultPageSize: 10,
        total: null,
        showQuickJumper: true
      },
      loading: false
    };
  },
  methods: {
    handleTableChange_zxxx(pageNumber) {
      this.fetch(pageNumber.current);
    },
    handleTableChange_ylxx(pageNumber) {
      this.fetch_ylxx(pageNumber.current);
    },
    showDrawer_ylgl() {
      this.fetch_ylxx(1);
      this.visible_ylgl = true;
    },
    showDrawer_tjfx() {
      this.visible_tjfx = true;
    },
    onClose() {
      this.visible_ylgl = false;
      this.visible_tjfx = false;
      this.visible_zxinfo = false;
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
    fetch_ylxx(pagenum) {
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
    click_zxinfo(key) {
      this.visible_zxinfo = true;
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
    },
    handleChange(info) {
      if (info.file.status !== "uploading") {
        // console.log(info.file, info.fileList);
      }
      if (info.file.status === "done") {
        this.$message.success(`${info.file.name} file uploaded successfully`);
        this.fileList = []; //也许可以清理掉已上传列表
      } else if (info.file.status === "error") {
        this.$message.error(`${info.file.name} file upload failed.`);
      }
    },
    init_char_cgl() {
      var chart = new G2.Chart({
        container: "char_cgl",
        forceFit: true,
        height: window.innerHeight,
        animate: false
      });
      chart.source(data_char_cgl, {
        percent: {
          formatter: function formatter(val) {
            val = val * 100 + "%";
            return val;
          }
        }
      });
      chart.coord("theta", {
        radius: 0.75,
        innerRadius: 0.6
      });
      chart.tooltip({
        showTitle: false,
        itemTpl:
          '<li><span style="background-color:{color};" class="g2-tooltip-marker"></span>{name}: {value}</li>'
      });
      // 辅助文本
      chart.guide().html({
        position: ["50%", "50%"],
        html:
          '<div style="color:#8c8c8c;font-size: 14px;text-align: center;width: 10em;">成功率</div>',
        alignX: "middle",
        alignY: "middle"
      });
      var interval = chart
        .intervalStack()
        .position("percent")
        .color("item")
        .label("percent", {
          formatter: function formatter(val, item) {
            return item.point.item + ": " + val;
          }
        })
        .tooltip("item*percent", function(item, percent) {
          percent = percent * 100 + "%";
          return {
            name: item,
            value: percent
          };
        })
        .style({
          lineWidth: 1,
          stroke: "#fff"
        });
      chart.render();
      interval.setSelected(data_char_cgl[0]);
    },
    init_char_tgl() {}
  }
};
</script>