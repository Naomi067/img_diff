<template>
    <div class="setResult">
      <el-page-header title="返回主页" fixed height="180px" :background-color="'#f5f5f5'" @back="goBack" v-if="showMessage"></el-page-header>
      <el-header> 当前对比版本 {{formattedOriginalVersion}} - {{formattedCompareVersion}}</el-header> 
        <div v-if="images.length">
            <div class="image">
                <img :src=currentImage :style="{ maxHeight: maxHeight + 'px' }" />
                <p>{{ currentImageName }}</p>
            </div>
            
            <div class="form"  v-if="showButton">
                <el-radio-group v-model="result">
                <el-radio :label="1">正常</el-radio>
                <el-radio :label="2">异常</el-radio>
                </el-radio-group>
            </div>
            <div class="button">
                <el-button type="primary" @click="submitResult" :disabled="!result" v-if="showButton">下一张</el-button>
                <div v-if="showMessage">当前版本{{formattedOriginalVersion}} - {{formattedCompareVersion}}的对比结果已全部确认</div>
            </div>
        </div>
        <div v-else>
            <!-- 这里是加载中的提示信息 -->
            <p>Loading...</p>
        </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'setResult',
    data() {
      return {
        images: [],
        currentImageIndex: 0,
        result: null,
        maxHeight: 0,
        showMessage: false,
        showButton: true,
        originalVersion: this.$route.params.originalVersion,
        compareVersion: this.$route.params.compareVersion,
      };
    },
    mounted() {
      this.maxHeight = window.innerHeight - 200;
      axios.get(`/api/get_version_abnormal_images?originalVersion=${this.$route.params.originalVersion}&compareVersion=${this.$route.params.compareVersion}`)
      .then((response) => {
        this.images = response.data;
        console.log(this.images);
      })
      .catch((error) => {
        console.error(error);
      });
    },
    computed: {
      currentImage() {
        if (this.images && this.images.length && this.images[this.currentImageIndex]) {
            const imageUrl = require( '/public/images/'+this.images[this.currentImageIndex].dir_name+'/'+this.images[this.currentImageIndex].name+'.jpg');
            return imageUrl;
        } else {
            return '';
        }
      },
      currentImageName() {
        if (this.images && this.images.length && this.images[this.currentImageIndex]) {
            return this.images[this.currentImageIndex].name;
        } else {
            return '';
        }
      },
      formattedOriginalVersion() {
        const date = new Date(this.originalVersion * 1000);
        return this.originalVersion.toString()+'['+date.toLocaleString()+']';
      },
      formattedCompareVersion() {
        const date = new Date(this.compareVersion * 1000);
        return this.compareVersion.toString()+'['+date.toLocaleString()+']';
      },
    },
    methods: {
      submitResult() {
        let data = {
          image_name: this.currentImageName,
          image_anomaly: this.result,
          image_version_ori: this.$route.params.originalVersion,
          image_version_tar: this.$route.params.compareVersion,
        };
        axios.post('/webapi/set_confirm', data)
          .then(response => {
            console.log(response);
            if (this.currentImageIndex < this.images.length - 1) {
              this.currentImageIndex++;
            }else {
              let ver_data = {
                image_version_ori: this.$route.params.originalVersion,
                image_version_tar: this.$route.params.compareVersion,
              };
              this.showButton = false;
              this.showMessage = true;
              axios.post('/webapi/confirmed_version', ver_data)
              .then(response => {
                console.log(response);
              })
              .catch((error) => {
                console.error(error.response.data);
              });
            }
            this.result = null;
          })
          .catch((error) => {
            console.error(error.response.data);
          });
      },
      goBack() {
        console.log('go back');
        this.$router.push('/');
      },
    },
  };
  </script>
  
  <style>
  .image-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 50px;
  }
  .image {
    text-align: center;
    margin-bottom: 20px;
  }
  .form {
    margin-right: 20px;
  }
  .button {
    margin-top: 20px;
  }
</style>