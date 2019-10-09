<template>
  <a-table :columns="columns" :dataSource="list_ttt">
    <a slot="name" slot-scope="text" href="javascript:;">{{text}}</a>
    <span slot="customTitle"><a-icon type="smile-o" /></span>
    <span slot="tags" slot-scope="tags">
      <a-tag v-for="tag in tags" color="blue" :key="tag">{{tag}}</a-tag>
    </span>
    <span slot="action">
      <a href="javascript:;">详情</a>
      <a-divider type="vertical"/>
      <a href="javascript:;">删除</a>
    </span>
  </a-table>
</template>



<script>
const columns = [{
  title: '编号',
  dataIndex: 'zxbh',
  key: 'zxbh',
}, {
  title: '名称',
  dataIndex: 'ylmc',
  key: 'ylmc',
}, {
  title: '执行时间',
  dataIndex: 'zxsj',
  key: 'zxsj',
}, {
  title: '覆盖率',
  key: 'fgl',
  dataIndex: 'fgl',
},{
  title: '成功率',
  key: 'cgl',
  dataIndex: 'cgl',
},{
  title: '通过率',
  key: 'tgl',
  dataIndex: 'tgl',
}, {
  title: '操作',
  key: 'action',
  scopedSlots: { customRender: 'action' },
}];



export default {
  name: "list",
  data() {
    return {
      list_ttt: [],
      columns
    };
  },
  methods: {
    getzxxx() {
      this.$http.get("http://localhost:8585/testurl2/zx_list/1")
        .then(function(response) {
          this.list_ttt = response.body.reslist;
        });
    }
  },
  created(){
      this.getzxxx()
  }
};
</script>