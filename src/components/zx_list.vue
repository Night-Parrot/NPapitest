<template>
  <a-table :columns="columns" :dataSource="list_ttt.reslist" :pagination="pagination"
    :loading="loading"
    @change="handleTableChange">
    <span ><a-icon type="smile-o" /></span>
    <span slot="tags">
    </span>
    <span slot="action">
      <a-button type="primary" :loading="loading">详情</a-button>
      <a-divider type="vertical"/>
      <a-button type="primary" :loading="loading">删除</a-button>
    </span>
  </a-table>
</template>



<script>
const columns = [{
  title: '编号',
  dataIndex: 'zxbh',
  key: 'zxbh',
  width: 100,
  align: 'center'
}, {
  title: '名称',
  dataIndex: 'ylmc',
  key: 'ylmc',
  width: 400,
  align: 'center'
  
}, {
  title: '执行时间',
  dataIndex: 'zxsj',
  key: 'zxsj',
  width: 400,
  align: 'center'
}, {
  title: '覆盖率',
  key: 'fgl',
  dataIndex: 'fgl',
  width: 200,
  align: 'center'
},{
  title: '成功率',
  key: 'cgl',
  dataIndex: 'cgl',
  width: 200,
  align: 'center'
},{
  title: '通过率',
  key: 'tgl',
  dataIndex: 'tgl',
  width: 200,
  align: 'center'
}, {
  title: '操作',
  key: 'action',
  scopedSlots: { customRender: 'action' },
  align: 'center'
}];



export default {
  name: "list",
  data() {
    return {
      list_ttt: [],
      columns,
      loading: false
    };
  },
  methods: {
    getzxxx() {
      this.$http.get("http://localhost:8585/testurl2/zx_list/1")
        .then(function(response) {
          this.list_ttt = response.body;
        });
    }
  },
  created(){
      this.getzxxx()
  },
  enterLoading () {
      this.loading = true
    },
    handleTableChange (pagination, filters, sorter) {
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;
      this.fetch({
        results: pagination.pageSize,
        page: pagination.current,
        sortField: sorter.field,
        sortOrder: sorter.order,
        ...filters,
      });
    }
};
</script>