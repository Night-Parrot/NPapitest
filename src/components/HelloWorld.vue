<template>
  <div>
    <div style="float: left;margin-left: 15px;width: 15%;margin-top: 15px;">
      <a-table :dataSource="data" :columns="columns" :pagination="pagination" :scroll="{ y: 840}" :rowKey="record => record.key">
        <!-- slot-scope 用来绑定record -->
        <router-link :to="{ path: '/xm_info/' + record.key }" slot="name" slot-scope="text, record">{{text}}</router-link>
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
import G2 from "@antv/g2";
export default {
  mounted() {
    this.init_fgl();
    this.init_tgl();
  },
  data() {
    return {
      data: [
        {
          key: "qweqweqweqwe",
          name: "T3C-立案",
          age: 32,
          address: "New York No. 1 Lake Park"
        },
        {
          key: "testurl2",
          name: "T3C-审判",
          age: 42,
          address: "London No. 1 Lake Park"
        },
        {
          key: "3",
          name: "T3C-诉费",
          age: 32,
          address: "Sidney No. 1 Lake Park"
        },
        {
          key: "4",
          name: "节约化执行",
          age: 32,
          address: "London No. 2 Lake Park"
        },
        {
          key: "5",
          name: "John Brown",
          age: 32,
          address: "New York No. 1 Lake Park"
        },
        {
          key: "6",
          name: "Joe Black",
          age: 42,
          address: "London No. 1 Lake Park"
        },
        {
          key: "7",
          name: "Jim Green",
          age: 32,
          address: "Sidney No. 1 Lake Park"
        },
        {
          key: "8",
          name: "Jim Red",
          age: 32,
          address: "London No. 2 Lake Park"
        },
        {
          key: "9",
          name: "Jim Red",
          age: 32,
          address: "London No. 2 Lake Park"
        },
        {
          key: "10",
          name: "John Brown",
          age: 32,
          address: "New York No. 1 Lake Park"
        },
        {
          key: "11",
          name: "Joe Black",
          age: 42,
          address: "London No. 1 Lake Park"
        },
        {
          key: "12",
          name: "Jim Green",
          age: 32,
          address: "Sidney No. 1 Lake Park"
        },
        {
          key: "13",
          name: "Jim Red",
          age: 32,
          address: "London No. 2 Lake Park"
        },
        {
          key: "14",
          name: "John Brown",
          age: 32,
          address: "New York No. 1 Lake Park"
        },
        {
          key: "15",
          name: "Joe Black",
          age: 42,
          address: "London No. 1 Lake Park"
        },
        {
          key: "16",
          name: "Jim Green",
          age: 32,
          address: "Sidney No. 1 Lake Park"
        },
        {
          key: "17",
          name: "Jim Red",
          age: 32,
          address: "London No. 2 Lake Park"
        },
        {
          key: "18",
          name: "John Brown",
          age: 32,
          address: "New York No. 1 Lake Park"
        },
        {
          key: "19",
          name: "Joe Black",
          age: 42,
          address: "London No. 1 Lake Park"
        },
        {
          key: "20",
          name: "Jim Green",
          age: 32,
          address: "Sidney No. 1 Lake Park"
        },
        {
          key: "21",
          name: "Jim Red",
          age: 32,
          address: "London No. 2 Lake Park"
        },
        {
          key: "22",
          name: "Jim Red",
          age: 32,
          address: "London No. 2 Lake Park"
        },
        {
          key: "23",
          name: "John Brown",
          age: 32,
          address: "New York No. 1 Lake Park"
        },
        {
          key: "24",
          name: "Joe Black",
          age: 42,
          address: "London No. 1 Lake Park"
        },
        {
          key: "25",
          name: "Jim Green",
          age: 32,
          address: "Sidney No. 1 Lake Park"
        },
        {
          key: "26",
          name: "Jim Red",
          age: 32,
          address: "London No. 2 Lake Park"
        }
      ],
      searchText: "",
      searchInput: null,
      columns: [
        {
          title: "项目名称",
          dataIndex: "name",
          key: "name",
          align: "center",
          width: "200",
          scopedSlots: {
            filterDropdown: "filterDropdown",
            filterIcon: "filterIcon",
            customRender: "name"
          },
          onFilter: (value, record) =>
            record.name.toLowerCase().includes(value.toLowerCase()),
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
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "2",
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "3",
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "4",
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "5",
          name: "T3C-立案",
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
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "2",
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "3",
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "4",
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        },
        {
          key: "5",
          name: "T3C-立案",
          ylmc: "立案流程V2.5.4-新增当事人",
          tgl: "65%",
          fgl: "95%",
          time: "2019-10-10 13:55:22"
        }
      ],
      pagination: {
        hideOnSinglePage: true,
        defaultPageSize: 500
      },
      chart_data_c: [
        { genre: "集约化执行T3E", sold: "100%", num: 100 },
        { genre: "执行救助", sold: "95.65%", num: 95.65 },
        { genre: "T3C立案", sold: "92.65%", num: 92.65 },
        { genre: "T3C审判", sold: "85.65%", num: 85.65 },
        { genre: "T3C审批", sold: "75%", num: 75 },
        { genre: "T3C案件信息", sold: "72.3%", num: 72.3 },
        { genre: "T3C诉讼费", sold: "72.3%", num: 72.3 },
        { genre: "港澳台", sold: "72.3%", num: 72.3 },
        { genre: "异地执行", sold: "72.3%", num: 72.3 },
        { genre: "司法辅助", sold: "72.3%", num: 72.3 }
      ],
      chart_data_d: [
        { genre: "集约化执行T3E", sold: "100%", num: 100 },
        { genre: "执行救助", sold: "95.65%", num: 95.65 },
        { genre: "T3C立案", sold: "92.65%", num: 92.65 },
        { genre: "T3C审判", sold: "85.65%", num: 85.65 },
        { genre: "T3C审批", sold: "75%", num: 75 },
        { genre: "T3C案件信息", sold: "72.3%", num: 72.3 },
        { genre: "T3C诉讼费", sold: "72.3%", num: 72.3 },
        { genre: "港澳台", sold: "72.3%", num: 72.3 },
        { genre: "异地执行", sold: "72.3%", num: 72.3 },
        { genre: "司法辅助", sold: "72.3%", num: 72.3 }
      ]
    };
  },
  methods: {
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
      alert("key:" + key)
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