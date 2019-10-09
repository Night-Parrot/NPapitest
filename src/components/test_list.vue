<template>
  <div>
    <div style="text-align: left;margin-top: 10px;margin-bottom: 10px;">
      <button>用例管理</button> |
      <button>统计分析</button>
    </div>
    <div>
      <table border="2" style="border:1px solid black;">
        <tbody>执行情况</tbody>
        <th>序号</th>
        <th>名称</th>
        <th>执行时间</th>
        <th>覆盖率</th>
        <th>成功率</th>
        <th>通过率</th>
        <th>操作</th>
        <tr v-for="item in list_ttt.reslist" :key="item.zxbh">
          <td>{{item.zxbh}}</td>
          <td>{{item.ylmc}}</td>
          <td>{{item.zxsj}}</td>
          <td>{{item.fgl}}</td>
          <td>{{item.cgl}}</td>
          <td>{{item.tgl}}</td>
          <button>详情</button>
          <button>删除</button>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "list",
  data() {
    return {
      list_ttt: []
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
  }
};
</script>