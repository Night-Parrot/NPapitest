<template>
    <div>
        <div>
        <button>用例管理</button>  |  
        <button>统计分析</button>
        </div>
    <table border="2" style="border:1px solid black;">
        <tbody>执行情况</tbody>
        <th>序号</th>
        <th>名称</th>
        <th>执行时间</th>
        <th>覆盖率</th>
        <th>成功率</th>
        <th>通过率</th>
        <th>操作</th>
        <tr>
            <td>1</td>
            <td>2</td>
            <td>2</td>
            <td>2</td>
            <td>2</td>
            <td>2</td>
            <button style="background-color: #4CAF50;border: none;color: white;padding: 1px 5px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;">详情</button>
            <button>删除</button>
        </tr>
    </table>
    </div>
</template>

<script>
export default {
//   name: 'HelloWorld',
//   props: {
//     msg: String
//   }
}
</script>

<style scoped>
{

}
</style>