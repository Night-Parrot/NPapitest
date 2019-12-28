<template>
  <div>
    <div>
      <a-drawer
        title="SMD_TO_SQL"
        :placement="placement_smd2sql"
        :closable="true"
        @close="onClose"
        :visible="visible_smd2sql"
        :destroyOnClose="true"
        height="500"
      >
        <a-spin tip="···(╯￣Д￣)╯╘═╛  正在处理，请稍后···" :spinning="spinning_smd2sql">
          <div style="float: left;margin-left: 30px;">
            <a-upload :fileList="fileList" :remove="handleRemove" :beforeUpload="beforeUpload">
              <a-button :disabled="fileList.length === 1">
                <a-icon type="upload" />请上传SMD文件
              </a-button>
            </a-upload>
          </div>
          <div style="float: left;">
            <a-button
              type="primary"
              @click="handleUpload"
              :disabled="fileList.length === 0"
              :loading="uploading_smd2sql"
              style="margin-left: 20px"
            >{{uploading_smd2sql ? '正在上传' : '上传' }}</a-button>
          </div>
        </a-spin>
      </a-drawer>
    </div>

    <div style="margin-left: 25px">
      <a-card
        hoverable
        style="width: 300px;float: left;margin: 25px 15px 15px 15px"
        @click="click_test"
      >
        <img
          alt="example"
          src="../assets/test_img.png"
          slot="cover"
        />
        <template class="ant-card-actions" slot="actions">
          <a-icon type="tool" theme="filled" style="fontSize: 25px" :spin="true" />
        </template>
        <a-card-meta title="SMD生成sql文件" description="提供人：尹熙文">
          <a-avatar
            slot="avatar"
            src="http://pics.sc.chinaz.com/Files/pic/icons128/dy_11/Insigne.png"
          />
        </a-card-meta>
      </a-card>
      <a-card hoverable style="width: 300px;float: left;margin: 25px 15px 15px 15px">
        <img
          alt="example"
          src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
          slot="cover"
        />
        <template class="ant-card-actions" slot="actions">
          <a-icon type="warning" theme="filled" style="fontSize: 25px" :spin="true" />
        </template>
        <a-card-meta title="···施工中···" description="敬请期待ε=(´ο｀*)))">
          <a-avatar
            slot="avatar"
            src="http://pics.sc.chinaz.com/Files/pic/icons128/dy_11/Insigne.png"
          />
        </a-card-meta>
      </a-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      visible_smd2sql: false,
      placement_smd2sql: "top",
      fileList: [],
      spinning_smd2sql: false,
      uploading_smd2sql: false
    };
  },
  methods: {
    click_test() {
      this.visible_smd2sql = !this.visible_smd2sql;
    },
    onClose() {
      this.visible_smd2sql = !this.visible_smd2sql;
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
      fileList.forEach(file => {
        formData.append("file", file);
      });
      this.uploading_smd2sql = !this.uploading_smd2sql;
      this.spinning_smd2sql = !this.spinning_smd2sql;
      axios
        .post("tool_smd2sql", formData, {
          headers: { "Content-Type": "multipart/form-data", Accept: "*/*" },
          responseType: "blob"
        })
        .then(res => {
          if (res.headers["content-type"] === 'application/json'){
            this.$message.error("格式错误或其他错误，请联系管理员");
            this.fileList = [];
            this.uploading_smd2sql = !this.uploading_smd2sql;
            this.spinning_smd2sql = !this.spinning_smd2sql;
          }else {
          let blob = new Blob([res.data], {
            type: res.headers["content-type"]
          });
          let downloadElement = document.createElement("a");
          let href = window.URL.createObjectURL(blob); // 创建下载的链接
          downloadElement.href = href;
          document.body.appendChild(downloadElement);
          downloadElement.click(); // 点击下载
          document.body.removeChild(downloadElement); // 下载完成移除元素
          window.URL.revokeObjectURL(href); // 释放掉blob对象
          this.fileList = [];
          this.uploading_smd2sql = !this.uploading_smd2sql;
          this.spinning_smd2sql = !this.spinning_smd2sql;
          }
        });
    }
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