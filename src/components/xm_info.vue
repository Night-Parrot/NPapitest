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
        <div style="float: left; width: 100%">
          <div style="float: left;margin-left: 30px;">
            <a-upload :fileList="fileList" :remove="handleRemove" :beforeUpload="beforeUpload">
              <a-button :disabled="fileList.length === 1">
                <a-icon type="upload" />选择用例文件
              </a-button>
            </a-upload>
          </div>
          <div style="float: left;">
            <a-button
              type="primary"
              @click="handleUpload"
              :disabled="fileList.length === 0"
              :loading="uploading"
              style="margin-left: 20px"
            >{{uploading ? '正在上传' : '上传' }}</a-button>
          </div>
          <div>
            <a-table
              :columns="columns_yl"
              :rowKey="record => record.zxbh"
              :dataSource="data_yl"
              :pagination="pagination"
              :loading="loading"
              size="middle"
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
        </div>
      </a-drawer>
    </div>
    <!-- ============================================================================================================================= -->
    <!-- 详情的抽屉 -->
    <div style="float: left;">
      <a-drawer
        title="执行情况"
        :placement="placement"
        :closable="true"
        @close="onClose"
        :visible="visible_zxinfo"
        :destroyOnClose="true"
        height="900"
      >
        <div style="float: left;width: 24%;">
          <div id="char_xysj" style="float: left;"></div>
          <div id="char_cgl" style="float: left;"></div>
          <div id="char_tgl" style="float: left;"></div>
        </div>
        <div style="float: right;width: 75%;">
          <a-radio-group
            :value="target_key"
            @change="handleSizeChange"
            style="margin-left:5px;margin-right:5px;margin-top: 5px;margin-bottom: 5px"
          >
            <a-radio-button value="1">全部</a-radio-button>
            <a-radio-button value="2">请求成功</a-radio-button>
            <a-radio-button value="3">请求失败</a-radio-button>
            <a-radio-button value="4">验证通过</a-radio-button>
            <a-radio-button value="5">验证失败</a-radio-button>
          </a-radio-group>
          <a-table
            :columns="columns_zxinfo"
            :dataSource="data_zxinfo"
            class="components-table-demo-nested"
            :scroll="{y:700}"
            size="middle"
            style="margin-left:5px;margin-right:5px;"
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
    <!-- 生成用例的抽屉 -->
    <div>
      <a-drawer
        title="用例生成模板"
        :placement="placement_ylsc"
        :closable="true"
        @close="onClose"
        :visible="visible_ylsc"
        :destroyOnClose="true"
        height="600"
      >
        <div>
          <a-input placeholder="请输入swagger地址" style="margin-top: 20px" />
          <a-input placeholder="如有需要，请输入cookie" style="margin-top: 20px" />
          <a-button type="primary" style="margin-top: 20px">生成用例</a-button>
        </div>
      </a-drawer>
    </div>

    <!-- =============================================================================================================================== -->
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
      <a-divider type="vertical" />
      <a-button
        type="primary"
        :loading="loading"
        style="margin-top: 15px"
        @click="showDrawer_ylsc"
      >用例模板生成</a-button>
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
    name: "案件签收",
    platform: "/zx/ajqs",
    version: "355ms",
    upgradeNum: "2014-12-24 23:12:00",
    creator: "200",
    createdAt: "通过"
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
    date:
      "{'name': '张三', 'para': '35.65','name': '张三', 'para': '35.65','name': '张三', 'para': '35.65','name': '张三', 'para': '35.65'}",
    name:
      "{'name': '张三', 'para': '35.65','name': '张三', 'para': '35.65','name': '张三', 'para': '35.65','name': '张三', 'para': '35.65'}",
    upgradeNum:
      "{'name': '张三', 'para': '35.65','name': '张三', 'para': '35.65','name': '张三', 'para': '35.65','name': '张三', 'para': '35.65'}"
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
      target_key: "1",
      data_char_cgl: data_char_cgl,
      columns_zxinfo: columns_zxinfo,
      innerColumns_zxinfo: innerColumns_zxinfo,
      data_zxinfo: data_zxinfo,
      innerData_zxinfo: innerData_zxinfo,
      char_xysj: [
        {
          date: "接口111",
          actual: 175,
          expected: 400
        },
        {
          date: "接口222",
          actual: 137,
          expected: 400
        },
        {
          date: "2017年3月4日",
          actual: 240,
          expected: 400
        },
        {
          date: "2017年3月5日",
          actual: 726,
          expected: 400
        },
        {
          date: "2017年3月6日",
          actual: 968,
          expected: 400
        },
        {
          date: "2017年3月7日",
          actual: 702,
          expected: 400
        },
        {
          date: "2017年3月8日",
          actual: 655,
          expected: 400
        },
        {
          date: "2017年3月9日",
          actual: 463,
          expected: 400
        },
        {
          date: "2017年3月10日",
          actual: 464,
          expected: 400
        },
        {
          date: "2017年3月12日",
          actual: 12,
          expected: 400
        },
        {
          date: "2017年3月13日",
          actual: 638,
          expected: 400
        },
        {
          date: "2017年3月14日",
          actual: 101,
          expected: 400
        },
        {
          date: "2017年3月15日",
          actual: 202,
          expected: 400
        },
        {
          date: "2017年3月16日",
          actual: 509,
          expected: 400
        },
        {
          date: "2017年3月17日",
          actual: 269,
          expected: 400
        },
        {
          date: "2017年3月18日",
          actual: 321,
          expected: 400
        },
        {
          date: "2017年3月19日",
          actual: 235,
          expected: 400
        },
        {
          date: "2017年3月20日",
          actual: 399,
          expected: 400
        },
        {
          date: "2017年3月21日",
          actual: 662,
          expected: 400
        },
        {
          date: "2017年3月22日",
          actual: 689,
          expected: 400
        },
        {
          date: "2017年3月23日",
          actual: 347,
          expected: 400
        },
        {
          date: "2017年3月24日",
          actual: 1485,
          expected: 400
        },
        {
          date: "2017年3月26日",
          actual: 428,
          expected: 400
        },
        {
          date: "2017年3月27日",
          actual: 749,
          expected: 400
        },
        {
          date: "2017年3月28日",
          actual: 752,
          expected: 400
        },
        {
          date: "2017年3月29日",
          actual: 658,
          expected: 400
        },
        {
          date: "2017年3月30日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月31日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月32日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月33日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月34日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月35日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月36日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月37日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月38日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月39日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月40日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月41日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月42日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月43日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月44日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月45日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月46日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月47日",
          actual: 69.1,
          expected: 400
        },
        {
          date: "2017年3月48日",
          actual: 669.1,
          expected: 400
        },
        {
          date: "2017年3月50日",
          actual: 169.1,
          expected: 400
        }
      ],
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
      visible_ylsc: false,
      fileList: [],
      uploading: false,
      placement: "top",
      placement_ylsc: "bottom",
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
    showDrawer_ylsc() {
      this.visible_ylsc = true;
    },
    onClose() {
      this.visible_ylgl = false;
      this.visible_tjfx = false;
      this.visible_zxinfo = false;
      this.visible_ylsc = false;
      this.fileList = [];
      this.uploading = false;
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
      this.target_key = "1";
      setTimeout(() => {
        this.init_char_cgl(), this.init_char_tgl(), this.init_char_xysj();
      }, 500);
      // this.init_char_cgl();
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
    init_char_cgl() {
      console.log("++++++++++++++++++++++");
      var chart = new G2.Chart({
        container: "char_cgl",
        // forceFit: true,
        height: 250,
        width: 465,
        animate: true
      });
      chart.source(this.data_char_cgl, {
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
    init_char_tgl() {
      console.log("++++++++++++++++++++++");
      var chart = new G2.Chart({
        container: "char_tgl",
        // forceFit: true,
        height: 250,
        width: 465,
        animate: true
        // padding: [50, 250, 50, 50],
      });
      chart.source(this.data_char_cgl, {
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
          '<div style="color:#8c8c8c;font-size: 14px;text-align: center;width: 10em;">通过率</div>',
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
    init_char_xysj() {
      var chart = new G2.Chart({
        container: "char_xysj",
        height: 300,
        width: 465,
        padding: [0, 100, 60, 100]
      });
      chart.source(this.char_xysj, {
        expected: {
          ticks: [0, 400, 1200]
        }
      });
      chart.axis("date", false);
      chart.axis("actual", false);
      chart.axis("expected", {
        line: null,
        tickLine: null,
        position: "right",
        label: {
          formatter: function formatter(val) {
            if (val === "1200") {
              return "";
            }
            return val;
          }
        }
      });
      chart.legend(false);
      chart
        .interval()
        .position("date*expected")
        .color("#87CEFA")
        .shape("borderRadius")
        .tooltip("expected")
        .opacity(0.6);
      chart
        .interval()
        .position("date*actual")
        .color("#db0d2d")
        .tooltip("actual")
        .shape("date*actual", function(date, val) {
          if (val === 0) {
            return;
          } else {
            return "borderRadius";
          }
        });
      chart.guide().text({
        position: ["min", "min"],
        content: "响应时间分布",
        style: {
          fill: "#ff2c55",
          fontSize: 20,
          fontWeight: "bold",
          textBaseline: "top"
        }
      });
      chart.render();
    },
    handleSizeChange(e) {
      this.target_key = e.target.value;
      console.log(e.target.value);
    },
    handleRemove(file) {
      const index = this.fileList.indexOf(file);
      const newFileList = this.fileList.slice();
      newFileList.splice(index, 1);
      this.fileList = newFileList;
    },
    beforeUpload(file) {
      this.fileList = [...this.fileList, file];
      return false;
    },
    handleUpload() {
      const { fileList } = this;
      const formData = new FormData();
      formData.append("xmdz", this.xmid);
      fileList.forEach(file => {
        formData.append("file", file);
      });
      this.uploading = true;
      this.$http
        .post("http://localhost:8585/uploadfile", formData, {
          headers: { "Content-Type": "multipart/form-data", Accept: "*/*" }
        })
        .then(function(res) {
          console.log(res.body);
          if (res.body.result === "success") {
            this.fileList = [];
            this.uploading = false;
            this.$message.success("上传成功");
          } else {
            this.fileList = [];
            this.uploading = false;
            this.$message.error(res.body.msg);
          }
        });
    }
  }
};
</script>