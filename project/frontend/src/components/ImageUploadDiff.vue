<template>
  <div class="ImageUpload">
    <border-titleVue :title="title">
      <label class="el-form-item__label" style="width: 100px;">
        图片文件
      </label>
      <el-upload
              v-model="fileList"
              ref="uploadref"
              action="#"
              :auto-upload="false"
              list-type="picture-card"
              :file-list="fileList"
              :limit="1"
              :on-change="handleChange"
              :on-preview="handlePictureCardPreview"
              :on-remove="handleRemove"
          >
              <i class="el-icon-plus"></i>
      </el-upload>
      <el-dialog v-model="dialogVisible">
              <img width="100%" :src="dialogImageUrl" alt="" />
      </el-dialog>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px">
        <el-form-item label="图片名称" prop="image_name">
          <el-input v-model="ruleForm.image_name" style="width: 300px"></el-input>
        </el-form-item>
        <el-form-item label="图片版本" prop="image_version">
          <el-input v-model="ruleForm.image_version" style="width: 300px"></el-input>
        </el-form-item>
        <el-form-item label="图片类型" prop="image_type">
          <el-input v-model="ruleForm.image_type" style="width: 300px"></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="submitForm('ruleForm')">上传图片</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </border-titleVue>
  </div>
</template>

<style>
    input[type="file"] {
        display: none;
    }
 
    .avatar-uploader .el-upload {
        border: 1px dashed #d9d9d9;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
 
    .avatar-uploader .el-upload:hover {
        border-color: #409EFF;
    }
 
    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 178px;
        height: 178px;
        line-height: 178px;
        text-align: center;
    }
 
    .avatar {
        width: 178px;
        height: 178px;
        display: block;
    }
</style>

<script>
import borderTitleVue from '@/components/borderTitle.vue'
export default {
  components: {
        borderTitleVue,
  },
  data() {
    return {
      ruleForm: {
          image_name: '',
          image_version: '',
          image_type: '',
      },
      rules: {
          image_name: [
              {required: true, message: '请输入图片名称', trigger: 'blur'},
          ],
          image_version: [
              {required: true, message: '请输入图片版本', trigger: 'blur'},
          ],
          image_type: [
              {required: true, message: '请输入图片类型', trigger: 'blur'},
          ],
      },
      param:new FormData(), //表单要提交的参数
      dialogImageUrl:"", //展示图片的地址
      fileList: [],
      dialogVisible: false,
      title:'比较图片',
    };
  },
  methods: {
    submitForm(formName) {
      var form = this.ruleForm;
      this.param.append('image_name', form.image_name);
      this.param.append('image_version', form.image_version);
      this.param.append('image_type', form.image_type);
      let config = {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
      };
      this.$axios.post('http://test.qa.leihuo.netease.com:9979/webapi/save-picture',this.param,config)
        .then(response=>{
          console.log(response.data);
        })
        .catch(function (error) {
        console.log(error);
        });
    },

    resetForm(formName) {
      this.$refs[formName].resetFields();
      this.ruleForm.imageUrl = '';
      this.param.image_url = '';
    },

    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },

    handleChange(file, fileList) {
      this.param.append("file", file["raw"]);
      this.param.append("fileName", file["name"]);
    },

    handleRemove(file, fileList) {
      console.log(file, fileList);
    },


  }
}
</script>