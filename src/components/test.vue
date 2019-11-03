<template>
  <a-form :form="form">
    <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="接口地址">
      <a-input v-decorator="[
          'url',
          { rules: [{ required: true, message: '接口地址不能为空' }] },
        ]" placeholder="请输入swagger-api-doc地址" />
    </a-form-item>
    <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="cookie">
      <a-input placeholder="如有需要，请输入cookie" v-decorator="[
          'cookie'
        ]" />
    </a-form-item>
    <a-form-item :label-col="formTailLayout.labelCol" :wrapper-col="formTailLayout.wrapperCol">
      <a-button type="primary" @click="check">
        生成用例
      </a-button>
    </a-form-item>
  </a-form>
</template>

<script>
  const formItemLayout = {
    labelCol: { span: 4 },
    wrapperCol: { span: 8 },
  };
  const formTailLayout = {
    labelCol: { span: 4 },
    wrapperCol: { span: 8, offset: 4 },
  };
  export default {
    data() {
      return {
        formItemLayout,
        formTailLayout,
        form: this.$form.createForm(this, { name: 'dynamic_rule' }),
      };
    },
    methods: {
      check() {
        this.form.validateFields((err, values) => {
          if (!err) {
            console.log(values);
          }
        });
      },
    },
  };
</script>