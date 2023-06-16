<template>
  <div class="ImageGalleryForm">
    <el-form :model="form" :rules="rules" ref="form" label-position="right" label-width="100px" style="margin-bottom: 20px;">
      <el-form-item label="原图版本"> 
        <el-select v-model="form.originalVersion" placeholder="请选择原图版本"> 
          <el-option v-for="version in ori_version_list" :key="version.id" :label="version.name" :value="version.name">
          </el-option> 
        </el-select> 
      </el-form-item> 
      <el-form-item label="对比版本"> 
        <el-select v-model="form.compareVersion" placeholder="请选择对比版本"> 
          <el-option v-for="version in tar_version_list" :key="version.id" :label="version.name" :value="version.name">
          </el-option> 
        </el-select> 
      </el-form-item> 
      <el-form-item> 
        <el-button type="primary" @click="handleSubmit">确认</el-button> 
      </el-form-item> 
    </el-form>
  </div>
</template>

<script>
import { Message } from 'element-ui';
export default {
  data() {
    return {
      form: {
        originalVersion: '',
        compareVersion: ''
      },
      ori_version_list: [],
      tar_version_list: [],
    }
  },
  methods: {
    async getVersions() {
      // 调用API获取版本信息
      const response = await fetch('api/get_versions')
      const data = await response.json()
      this.ori_version_list = data["ori_version_list"]
      this.tar_version_list = data["tar_version_list"]
      console.log(data)
    },
    handleSubmit() {
      console.log(this.form)
      if (this.form.originalVersion !== null && this.form.originalVersion !== '' &&
    this.form.compareVersion !== null && this.form.compareVersion !== '') {
        // 表单数据不为空，执行相关逻辑
        console.log(this.form.originalVersion)
        console.log(this.form.compareVersion)
        this.$router.push({ name: 'Result', params: { originalVersion: this.form.originalVersion, compareVersion: this.form.compareVersion } })
      } else {
        // 表单数据为空，提示用户填写表单
        Message({
          message: '请选择原图版本和对比版本',
          type: 'warning',
          duration: 2000,
        });
      }
    },
  },
  mounted() {
    this.getVersions()
  }
}
</script>

<style> .select-panel { display: flex; justify-content: center; align-items: center; } </style>