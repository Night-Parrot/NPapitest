<template>
  <div>
    <!-- 用例信息的抽屉 -->
    <div>
      <a-drawer title="用例管理" :placement="placement" :closable="true" @close="onClose" :visible="visible_ylgl"
        :destroyOnClose="true" height="800">
        <div style="float: left; width: 100%">
          <div style="float: left;margin-left: 30px;">
            <a-upload :fileList="fileList" :remove="handleRemove" :beforeUpload="beforeUpload">
              <a-button :disabled="fileList.length === 1">
                <a-icon type="upload" />选择用例文件
              </a-button>
            </a-upload>
          </div>
          <div style="float: left;">
            <a-button type="primary" @click="handleUpload" :disabled="fileList.length === 0" :loading="uploading"
              style="margin-left: 20px">{{uploading ? '正在上传' : '上传' }}</a-button>
          </div>
          <div style="margin-top: 80px">
            <a-table :columns="columns_yl" :rowKey="record => record.ylbh" :dataSource="data_yl"
              :pagination="pagination_yl_list" :loading="loading_yl_list" size="middle" @change="handleTableChange_ylxx"
              style="margin-left: 30px;margin-right: 30px;">
              <H3 slot="title">用例列表</H3>
              <span slot="action_yl" slot-scope="record">
                <a-button type="primary" :loading="loading_runcanse" @click="click_info(record.ylbh)">执行</a-button>
                <a-divider type="vertical" />
                <a-button type="primary" :loading="loading_download" @click="click_dl_case(record.ylbh)">下载</a-button>
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
      <a-drawer title="统计分析" :placement="placement" :closable="true" @close="onClose" :visible="visible_tjfx"
        :destroyOnClose="true" height="800">
        <div>
          <h4>暂时没想好统计内容</h4>
        </div>
      </a-drawer>
    </div>
    <!-- ============================================================================================================================= -->
    <!-- 详情的抽屉 -->
    <div style="float: left;">
      <a-drawer title="执行情况" :placement="placement" :closable="true" @close="onClose" :visible="visible_zxinfo"
        :destroyOnClose="true" height="900">
        <a-spin :spinning="spinning" :delay="delayTime" tip="···用例仍在执行中，请保持冷静，页面会自动检查用例执行情况···">
          <div style="float: left;width: 24%;">
            <div id="char_xysj" style="float: left;"></div>
            <div id="char_cgl" style="float: left;"></div>
            <div id="char_tgl" style="float: left;"></div>
          </div>
          <div style="float: right;width: 75%;">
            <a-radio-group :value="target_key" @change="handleSizeChange"
              style="margin-left:5px;margin-right:5px;margin-top: 5px;margin-bottom: 5px">
              <a-radio-button value="1">全部</a-radio-button>
              <a-radio-button value="2">请求成功</a-radio-button>
              <a-radio-button value="3">请求失败</a-radio-button>
              <a-radio-button value="4">验证通过</a-radio-button>
              <a-radio-button value="5">验证失败</a-radio-button>
            </a-radio-group>
            <a-table :columns="columns_zxinfo" :dataSource="data_zxinfo" class="components-table-demo-nested"
              :scroll="{y:670}" size="middle" style="margin-left:5px;margin-right:5px;" :pagination="placement_zxinfo"
              :loading="loading_zxinfo" @change="handleTableChange_zxinfo">
              <a-table slot="expandedRowRender" slot-scope="record" :columns="innerColumns_zxinfo"
                :dataSource="record.innerlist" :rowKey="record => record.key" :pagination="false" size="small"
                style="margin-left: 15px;margin-right: 15px"></a-table>
            </a-table>
          </div>
        </a-spin>
      </a-drawer>
    </div>

    <!-- ============================================================================================================================= -->
    <!-- 生成用例的抽屉 -->
    <div>
      <a-drawer title="用例生成模板" :placement="placement_ylsc" :closable="true" @close="onClose" :visible="visible_ylsc"
        :destroyOnClose="true" width="600">
        <div>
          <a-form :form="form" style="margin-top: 10px">
            <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
              <a-input v-decorator="[
                  'url',
                  { rules: [{ required: true, message: '接口地址不能为空' }] },
                ]" placeholder="请输入swagger-api-doc地址" style="margin-top: 20px;text-align:center" />
            </a-form-item>
            <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
              <a-input placeholder="如有需要，请输入cookie" v-decorator="[
                  'cookie'
                ]" style="margin-top: 20px;text-align:center" />
            </a-form-item>
            <a-form-item :label-col="formTailLayout.labelCol" :wrapper-col="formTailLayout.wrapperCol">
              <a-button type="primary" style="margin-top: 20px;margin-left: 6px" :loading="loading_makecase" @click="casemake">
                生成用例
              </a-button>
            </a-form-item>
          </a-form>
        </div>
        <div>
          <h1>用例模板生成说明：</h1>
          <img preview='0' src='../assets/info.png' height='260' width='550' style="cursor:pointer"></img>
          <h2></h2>
          <h2>不要直接使用swagger地址</h2>
          <h2>在访问swagger页面的时候，查看所有请求</h2>
          <h2>返回全部接口数据的接口地址，才是可以使用的地址</h2>
          <h2>一般情况下包含api-docs的就是可以用来生成模板的地址</h2>
        </div>
      </a-drawer>
    </div>

    <!-- =============================================================================================================================== -->
    <div style="margin-left: 30px;">
      <a-button type="primary" :loading="loading" @click="showDrawer_ylgl" style="margin-top: 40px">用例管理</a-button>
      <a-divider type="vertical" />
      <a-button type="primary" :loading="loading" style="margin-top: 15px" @click="showDrawer_tjfx">统计分析</a-button>
      <a-divider type="vertical" />
      <a-button type="primary" :loading="loading" style="margin-top: 15px" @click="showDrawer_ylsc">用例模板生成</a-button>
    </div>
    <div>
      <a-table :columns="columns" :rowKey="record => record.zxbh" :dataSource="data.reslist"
        :pagination="pagination_zx_list" :loading="loading_list" @change="handleTableChange_zxxx"
        style="margin-left: 30px;margin-right: 30px;margin-top: 30px">
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
  import axios from "axios";

  const formItemLayout = {
    labelCol: { span: 5 },
    wrapperCol: { span: 25 },
  };
  const formTailLayout = {
    labelCol: { span: 4 },
    wrapperCol: { span: 8, offset: 10 },
  };

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
  // var data_char_all = [
  //   {
  //     item: "调用成功",
  //     count: 40,
  //     percent: 0.4
  //   },
  //   {
  //     item: "调用失败",
  //     count: 21,
  //     percent: 0.21
  //   }
  // ];

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
      dataIndex: "url",
      key: "url",
      align: "center",
      width: 300
    },
    {
      title: "响应时间",
      dataIndex: "xysj",
      key: "xysj",
      align: "center",
      width: 200
    },
    {
      title: "执行时间",
      dataIndex: "zxsj",
      key: "zxsj",
      align: "center",
      width: 100
    },
    {
      title: "接口状态",
      dataIndex: "jkzt",
      key: "jkzt",
      align: "center",
      width: 100
    },
    {
      title: "验证结果",
      dataIndex: "yzjg",
      key: "yzjg",
      align: "center",
      width: 200
    }
  ];

  const innerColumns_zxinfo = [
    {
      title: "参数",
      dataIndex: "cs",
      key: "cs",
      align: "center",
      width: 400
    },
    {
      title: "预期返回值",
      dataIndex: "yqfhz",
      key: "yqfhz",
      align: "center",
      width: 400
    },
    {
      title: "实际返回值",
      dataIndex: "sjfhz",
      key: "sjfhz",
      align: "center",
      width: 400
    }
  ];

  // =================================
  export default {
    mounted() {
      this.xmid = this.$route.params.xmid;
      //获取首页传递过来的项目地址，并赋值给当前页面，之后页面相关查询以该参数为主
      //实际应该拿主键过来，但是因为主键生成的地址不好看 (=^ ^=)，所以使用了项目地址，项目地址在数据库中不可重复，否则会造成页面混乱或者报错
      this.fetch(1);
    },
    data() {
      return {
        url: "",
        cookie: "",
        loading_runcanse: false,
        loading_makecase: false,
        loading_download: false, //下载用的
        target_key: "1",
        data_char_all: [],
        columns_zxinfo: columns_zxinfo,
        innerColumns_zxinfo: innerColumns_zxinfo,
        data_zxinfo: [],
        innerData_zxinfo: [],
        char_xysj: [],
        data: [],
        columns_yl: columns_yl,
        columns: columns,
        visible_zxinfo: false,
        data_yl: [],
        xmid: "",
        visible_ylgl: false,
        visible_tjfx: false,
        visible_ylsc: false,
        fileList: [],
        uploading: false,
        placement: "top",
        placement_ylsc: "right",
        pagination_zx_list: {
          defaultPageSize: 10,
          total: null,
          showQuickJumper: true,
          position: "bottom",
          current: 1
        },
        pagination_yl_list: {
          defaultPageSize: 8,
          total: null,
          showQuickJumper: true,
          position: "bottom",
          current: 1
        },
        placement_zxinfo: {
          defaultPageSize: 10,
          total: null,
          showQuickJumper: true,
          position: "bottom",
          current: 1
        },
        loading: false,
        loading_list: false,
        loading_yl_list: false,
        loading_zxinfo: false,
        spinning: false,
        delayTime: 50,
        zxid: "", // 记录当前打开的用例执行id
        formItemLayout, //生成用例的表单使用
        formTailLayout, //生成用例的表单使用
        form: this.$form.createForm(this, { name: 'dynamic_rule' }), //生成用例的表单使用
      };
    },
    methods: {
      handleTableChange_zxxx(pageNumber) {
        this.fetch(pageNumber.current);
      },
      handleTableChange_ylxx(pageNumber) {
        this.fetch_ylxx(pageNumber.current);
      },
      handleTableChange_zxinfo(pageNumber) {
        this.fetch_ylzxinfo(pageNumber.current);
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
        this.data_zxinfo = [];
        this.innerData_zxinfo = [];
        this.target_key = "1";
        this.placement_zxinfo.current = 1;
        this.zxid = "";
        this.loading_download = false;
      },
      fetch(pagenum) {
        this.loading_list = true;
        axios.get(this.xmid + "/zx_list/" + pagenum).then(response => {
          this.data = response.data;
          this.pagination_zx_list.total = response.data.maxsize;
          this.pagination_zx_list.current = pagenum; //用例执行记录的页码
        });
        this.loading_list = false;
      },
      fetch_ylxx(pagenum) {
        this.loading_yl_list = true;
        axios.get(this.xmid + "/yl_list/" + pagenum).then(response => {
          this.data_yl = response.data.reslist;
          this.pagination_yl_list.total = response.data.maxsize;
          this.pagination_yl_list.current = response.data.nowpage;
        });
        this.loading_yl_list = false;
      },
      fetch_ylzxinfo(pagenum) {
        //执行信息的详情获取
        this.loading_zxinfo = true;
        // this.spinning = true;
        axios
          .get("ylzx_info/" + this.zxid + "/" + pagenum, {
            params: { zt: this.target_key }
          })
          .then(response => {
            this.data_zxinfo = response.data.reslist;
            this.placement_zxinfo.total = response.data.maxsize;
            this.placement_zxinfo.current = pagenum;
            if (response.data.zt === "0") {
              setTimeout(() => {
                this.fetch_ylzxinfo(pagenum);
              }, 2000);
            } else {
              this.spinning = false;
            }
          });
        this.loading_zxinfo = false;
      },
      hhh() {
        alert("hhhhh");
      },
      click_info(key) {
        // 执行用例时的方法
        this.loading_runcanse = true;
        // this.$http
        axios
          .post(
            "runcase",
            { ylbh: key },
            {
              headers: { "Content-Type": "application/json", Accept: "*/*" }
            }
          )
          .then(res => {
            if (res.data.result === "success") {
              this.loading_runcanse = false;
              // this.$message.success("执行成功");
              this.visible_ylgl = false;
              this.click_zxinfo(res.data.zxid);
            } else {
              this.loading_runcanse = false;
              this.$message.error(res.data.msg);
            }
          });
        // 刷新用例列表，更新用例执行记录列表
        setTimeout(() => {
          this.fetch_ylxx(this.pagination_yl_list.current);
          this.fetch(1);
        }, 800);
      },
      click_zxinfo(key) {
        this.visible_zxinfo = true;
        this.spinning = true;
        this.zxid = key;
        this.fetch_ylzxinfo(this.placement_zxinfo.current);
        axios.get('tjxx', {params: {'zxid': key}}).then(response => {
          this.data_char_all = response.data;
        })
        axios.get('sjfb', {params: {'zxid': key}}).then(response => {
          this.char_xysj = response.data;
        })
        setTimeout(() => {
          this.init_char_cgl(), this.init_char_tgl(), this.init_char_xysj();
        }, 1000);
      },
      click_del(key) {
        alert("delkey:" + key);
      },
      init_char_cgl() {
        var chart = new G2.Chart({
          container: "char_cgl",
          // forceFit: true,
          height: 250,
          width: 465,
          // animate: true
        });
        chart.source(this.data_char_all[0], {
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
          .tooltip("item*count", function (item, count) {
            // percent = percent * 100 + "%";
            count = count + "个"
            return {
              name: item,
              value: count
            };
          })
          .style({
            lineWidth: 1,
            stroke: "#fff"
          });
        chart.render();
        // interval.setSelected(data_char_all[0][0]);
      },
      init_char_tgl() {
        var chart = new G2.Chart({
          container: "char_tgl",
          // forceFit: true,
          height: 250,
          width: 465,
          animate: true
          // padding: [50, 250, 50, 50],
        });
        chart.source(this.data_char_all[1], {
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
          .tooltip("item*count", function (item, count) {
            // percent = percent * 100 + "%";
            count = count + "个";
            return {
              name: item,
              value: count
            };
          })
          .style({
            lineWidth: 1,
            stroke: "#fff"
          });
        chart.render();
        // interval.setSelected(data_char_all[1][0]);
      },
      init_char_xysj() {
        console.log(this.char_xysj);
        
        var chart = new G2.Chart({
          container: "char_xysj",
          height: 300,
          width: 465,
          padding: [20, 100, 60, 100]
        });
        chart.source(this.char_xysj, {
          expected: {
            ticks: [0, 5000, 10000]
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
              if (val === "200") {
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
          .shape("date*actual", function (date, val) {
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
        this.fetch_ylzxinfo(1);
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
        axios
          .post("uploadfile", formData, {
            headers: { "Content-Type": "multipart/form-data", Accept: "*/*" }
          })
          .then(res => {
            if (res.data.result === "success") {
              this.fileList = [];
              this.uploading = false;
              this.$message.success("上传成功");
            } else {
              this.fileList = [];
              this.uploading = false;
              this.$message.error(res.data.msg);
            }
          });
        setTimeout(() => {
          this.fetch_ylxx(1);
          this.pagination_yl_list.current = 1;
        }, 400);
      },
      casemake() {
        this.loading_makecase = true;
        this.form.validateFields((err, values) => {
          if (!err) {
            console.log(values);
            axios({
              method: "get",
              url: "makecase",
              params: values,
              responseType: "blob"
            })
              .then( (response) => {
                // console.log(response.headers["content-type"]);
                if (response.headers["content-type"] != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") {
                  this.$message.error("用例生成失败，请检查填写的内容或联系管理员")
                }
                else {
                  let blob = new Blob([response.data], {
                    type: response.headers["content-type"]
                  });
                  let downloadElement = document.createElement("a");
                  let href = window.URL.createObjectURL(blob); // 创建下载的链接
                  downloadElement.href = href;
                  document.body.appendChild(downloadElement);
                  downloadElement.click(); // 点击下载
                  document.body.removeChild(downloadElement); // 下载完成移除元素
                  window.URL.revokeObjectURL(href); // 释放掉blob对象
                }
              });
          }
        });
        this.loading_makecase = false;
      },
      click_dl_case(ylbh) {
        this.loading_download = true;
        axios({
          method: "get",
          url: "/downloadfile/" + ylbh,
          responseType: "blob"
        }).then(response => {
          console.log(response);
          if (response.headers["content-type"] != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") {
            this.$message.error("用例下载失败，可能是文件损坏或丢失，请联系管理员")
          }
          else {

            let blob = new Blob([response.data], {
              type: response.headers["content-type"]
            });
            let downloadElement = document.createElement("a");
            let href = window.URL.createObjectURL(blob); // 创建下载的链接
            downloadElement.href = href;
            document.body.appendChild(downloadElement);
            downloadElement.click(); // 点击下载
            document.body.removeChild(downloadElement); // 下载完成移除元素
            window.URL.revokeObjectURL(href); // 释放掉blob对象
          }
        });
        this.loading_download = false;
      },
      check() {
        this.form.validateFields((err, values) => {
          if (!err) {
            console.log(values);
          }
        });
      },
    }
  };
</script>



<style scoped>
  .spin-content {
    border: 1px solid #91d5ff;
    background-color: #e6f7ff;
    padding: 30px;
  }

</style>