<template>
  <div>
    <a-button type="primary" style="float: right;margin-top: 10px; margin-right: 20px" :loading="loading_yhsc" @click="dl_yhsc">下载使用说明</a-button>
    <div style="float: left;margin-left: 15px;width: 15%;margin-top: 15px;">
      <a-table
        :dataSource="data"
        :columns="columns"
        :loading="loading"
        :pagination="pagination_xmlist"
        :scroll="{ y: 840}"
        :rowKey="record => record.xmbh"
      >
        <!-- slot-scope 用来绑定record -->
        <router-link
          :to="{ path: '/xm_info/' + record.xmdz }"
          slot="name"
          slot-scope="text, record"
        >{{text}}</router-link>
        <div
          slot="filterDropdown"
          slot-scope="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }"
          class="custom-filter-dropdown"
        >
          <a-input
            v-ant-ref="c => searchInput = c"
            :placeholder="`请输入${column.title}`"
            :value="selectedKeys[0]"
            @change="e => setSelectedKeys(e.target.value ? [e.target.value] : [])"
            @pressEnter="() => handleSearch(selectedKeys, confirm)"
            style="width: 188px; margin-bottom: 8px; display: block;"
          />
          <a-button
            type="primary"
            @click="() => handleSearch(selectedKeys, confirm)"
            icon="search"
            size="small"
            style="width: 90px; margin-right: 8px"
          >查询</a-button>
          <a-button
            @click="() => handleReset(clearFilters)"
            size="small"
            icon="reload"
            style="width: 90px"
          >清空</a-button>
        </div>
        <a-icon
          slot="filterIcon"
          slot-scope="filtered"
          type="search"
          :style="{ color: filtered ? '#108ee9' : undefined }"
        />
        <template slot="customRender" slot-scope="text">
          <span v-if="searchText">
            <template
              v-for="(fragment, i) in text.toString().split(new RegExp(`(?<=${searchText})|(?=${searchText})`, 'i'))"
            >
              <mark
                v-if="fragment.toLowerCase() === searchText.toLowerCase()"
                :key="i"
                class="highlight"
              >{{fragment}}</mark>
              <template v-else>{{fragment}}</template>
            </template>
          </span>
          <template v-else>{{text}}</template>
        </template>
      </a-table>
    </div>
    <div style="float: left;">
      <div style="float: left;margin-top: 50px;margin-left:20px;width: 45%;" id="app_c"></div>
      <div style="float: left;margin-top: 50px;margin-left:20px;width: 45%;" id="app_d"></div>
      <div>
        <div
          style="float: left;margin-top: 50px;margin-left:50px;margin-right:20px;width: 45%"
          id="app_e"
        >
          <h4>最近更新项目</h4>
          <a-table
            :columns="columns_xm"
            :dataSource="data_xm"
            size="small"
            style="margin-left: 15px;width: 100%;margin-top: 15px;"
            :pagination="pagination"
          />
        </div>
        <div style="float: left;margin-top: 50px;margin-left:15px;width: 45%">
          <h4>最近执行项目</h4>
          <a-table
            :columns="columns_zx"
            :dataSource="data_zx"
            size="small"
            style="margin-left: 15px;width: 100%;margin-top: 15px;"
            :pagination="pagination"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import G2 from "@antv/g2";
export default {
  mounted() {
    this.init_fgl();
    this.init_tgl();
    this.xm_list();
  },
  data() {
    return {
      data: [],
      loading: false,
      searchText: "",
      searchInput: null,
      loading_yhsc: false,
      columns: [
        {
          title: "项目名称",
          dataIndex: "xmmc",
          key: "xmmc",
          align: "center",
          width: "200",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "name"
          },
          onFilter: (value, record) =>
            record.xmmc.toLowerCase().includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: visible => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              }, 0);
            }
          }
        }
      ],
      columns_xm: [
        {
          title: "项目名称",
          dataIndex: "name"
        },
        {
          title: "用例名称",
          dataIndex: "ylmc"
        },
        {
          title: "上传时间",
          dataIndex: "time"
        }
      ],
      data_xm: [
        {
          key: "1",
          name: "项目1",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "2",
          name: "项目2",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "3",
          name: "项目3",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "4",
          name: "项目4",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "5",
          name: "项目5",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        }
      ],
      columns_zx: [
        {
          title: "项目名称",
          dataIndex: "name"
        },
        {
          title: "用例名称",
          dataIndex: "ylmc"
        },
        {
          title: "覆盖率",
          dataIndex: "fgl"
        },
        {
          title: "通过率",
          dataIndex: "tgl"
        },
        {
          title: "执行时间",
          dataIndex: "time"
        }
      ],
      data_zx: [
        {
          key: "xm_info",
          name: "项目1",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "2",
          name: "项目2",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "3",
          name: "项目3",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "4",
          name: "项目4",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "5",
          name: "项目5",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        }
      ],
      pagination_xmlist: {
        hideOnSinglePage: true,
        defaultPageSize: 500
      },
      pagination: {
        hideOnSinglePage: true,
        defaultPageSize: 500
      },
      chart_data_c: [
        { genre: "项目1", sold: "100%", num: 100 },
        { genre: "项目2", sold: "95.65%", num: 95.65 },
        { genre: "项目3", sold: "92.65%", num: 92.65 },
        { genre: "项目4", sold: "85.65%", num: 85.65 },
        { genre: "项目5", sold: "75%", num: 75 },
        { genre: "项目6", sold: "72.3%", num: 72.3 },
        { genre: "项目7", sold: "72.3%", num: 72.3 },
        { genre: "项目8", sold: "72.3%", num: 72.3 },
        { genre: "项目9", sold: "72.3%", num: 72.3 },
        { genre: "项目10", sold: "72.3%", num: 72.3 }
      ],
      chart_data_d: [
        { genre: "项目1", sold: "100%", num: 100 },
        { genre: "项目2", sold: "95.65%", num: 95.65 },
        { genre: "项目3", sold: "92.65%", num: 92.65 },
        { genre: "项目4", sold: "85.65%", num: 85.65 },
        { genre: "项目5", sold: "75%", num: 75 },
        { genre: "项目6", sold: "72.3%", num: 72.3 },
        { genre: "项目7", sold: "72.3%", num: 72.3 },
        { genre: "项目8", sold: "72.3%", num: 72.3 },
        { genre: "项目9", sold: "72.3%", num: 72.3 },
        { genre: "项目10", sold: "72.3%", num: 72.3 }
      ]
    };
  },
  methods: {
    xm_list() {
      this.loading = true;
      axios({ method: "get", url: "project_list" }).then(response => {
        this.data = response.data.reslist;
        this.pagination_xmlist.defaultPageSize = response.data.maxsize;
      });
      this.loading = false;
    },
    handleSearch(selectedKeys, confirm) {
      confirm();
      this.searchText = selectedKeys[0];
    },

    handleReset(clearFilters) {
      clearFilters();
      this.searchText = "";
    },

    init_fgl() {
      // 此函数为个人习惯,喜欢创建一个初始化的函数
      const chart = new G2.Chart({
        container: "app_c",
        width: 750,
        height: 450,
        padding: [10, 120, 40, 120]
      });
      chart.source(this.chart_data_c, { value: { alias: "覆盖率前十的项目" } });
      chart.axis("value", {
        // 这部分尚未生效，有待排查
        label: null,
        title: {
          offset: 30,
          textStyle: {
            fontSize: 10,
            fontWeight: 600
          }
        }
      });
      chart.coord().transpose();
      chart
        .interval()
        .position("genre*num")
        .size(20)
        .label("sold", {
          textStyle: {
            fill: "#8d8d8d"
          },
          offset: 10
        });
      this.chart = chart;
      this.chart.render();
    },
    init_tgl() {
      // 此函数为个人习惯,喜欢创建一个初始化的函数
      const chart = new G2.Chart({
        container: "app_d",
        width: 750,
        height: 450,
        padding: [10, 120, 40, 120]
      });
      chart.source(this.chart_data_d, { value: { alias: "覆盖率前十的项目" } });
      chart.axis("value", {
        // 这部分尚未生效，有待排查
        label: null,
        title: {
          offset: 30,
          textStyle: {
            fontSize: 10,
            fontWeight: 600
          }
        }
      });
      chart.coord().transpose();
      chart
        .interval()
        .position("genre*num")
        .size(20)
        .label("sold", {
          textStyle: {
            fill: "#8d8d8d"
          },
          offset: 10
        });
      this.chart = chart;
      this.chart.render();
    },
    zx_info(key) {
      // alert("这是点击事件")
      alert("key:" + key);
    },
    dl_yhsc() {
      this.loading_yhsc = true;
      axios.get('downloadyhsc', {responseType: 'blob'}).then(response=>{
        console.log(response);
        
        let blob = new Blob([response.data], {
          type: response.headers["content-type"]
        });
        let downloadElement = document.createElement("a");
        let href = window.URL.createObjectURL(blob); // 创建下载的链接
        downloadElement.href = href;
        downloadElement.download = '使用手册.docx'
        document.body.appendChild(downloadElement);
        downloadElement.click(); // 点击下载
        document.body.removeChild(downloadElement); // 下载完成移除元素
        window.URL.revokeObjectURL(href); // 释放掉blob对象
      });
      this.loading_yhsc =false;
    }
  }
};
</script>
<style scoped>
.custom-filter-dropdown {
  padding: 8px;
  border-radius: 4px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
</style>