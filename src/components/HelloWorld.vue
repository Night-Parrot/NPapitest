<template>
  <div>
    <div style="float: left;margin-left: 15px;width: 15%;margin-top: 15px;">
      <a-table :dataSource="data" :columns="columns" :pagination="pagination" :scroll="{ y: 840}">
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
    <div style="float: left;margin-top: 40px;margin-left:15px" id="app_c"></div>
    <div style="float: left;margin-top: 15px;margin-left:15px" id="app_d"></div>
  </div>
</template>

<script>
import G2 from "@antv/g2";
const data = [
  {
    key: "1",
    name: "John Brown",
    age: 32,
    address: "New York No. 1 Lake Park"
  },
  {
    key: "2",
    name: "Joe Black",
    age: 42,
    address: "London No. 1 Lake Park"
  },
  {
    key: "3",
    name: "Jim Green",
    age: 32,
    address: "Sidney No. 1 Lake Park"
  },
  {
    key: "4",
    name: "Jim Red",
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
];

export default {
  mounted() {
    this.initComponent();
  },
  data() {
    return {
      data,
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
            customRender: "customRender"
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
      pagination: {
        hideOnSinglePage: true,
        defaultPageSize: 500
      },
      chart_data_c: [
        { genre: "集约化执行T3E", sold: 275 },
        { genre: "执行救助", sold: 32 },
        { genre: "T3C立案", sold: 222 },
        { genre: "T3C审判", sold: 215 },
        { genre: "T3C审批", sold: 200 },
        { genre: "T3C案件信息", sold: 150 },
        { genre: "T3C诉讼费", sold: 120 },
        { genre: "港澳台", sold: 95 },
        { genre: "异地执行", sold: 66 },
        { genre: "司法辅助", sold: 11 }
      ],
      chart_data_d: [
        { genre: "集约化执行T3E", sold: 275 },
        { genre: "执行救助", sold: 32 },
        { genre: "T3C立案", sold: 222 },
        { genre: "T3C审判", sold: 215 },
        { genre: "T3C审批", sold: 200 },
        { genre: "T3C案件信息", sold: 150 },
        { genre: "T3C诉讼费", sold: 120 },
        { genre: "港澳台", sold: 95 },
        { genre: "异地执行", sold: 66 },
        { genre: "司法辅助", sold: 11 }
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

    initComponent() {
      // 此函数为个人习惯,喜欢创建一个初始化的函数
      const chart = new G2.Chart({
        container: "app_c",
        width: 750,
        height: 450,
      });
      chart.source(this.chart_data_c, {value: {alisa: "覆盖率前十的项目"}});
      chart.coord().transpose();
      chart
        .interval()
        .position("genre*sold")
        .size(20)
        .label("sold", {
          textStyle: {
            fill: "#8d8d8d"
          },
          offset: 10
        });
      // .color("genre");
      this.chart = chart;
      this.chart.render();
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