<template>
    <div class="getResult">
      <el-page-header title="返回主页" fixed height="180px" :background-color="'#f5f5f5'" @back="goBack" ></el-page-header>
      <el-header> 当前对比版本 {{formattedOriginalVersion}} - {{formattedCompareVersion}}</el-header>
        <div v-if="images.length">
            <div class="image">
                <img :src=currentImage :style="{ maxHeight: maxHeight + 'px' }" />
                <p>{{ currentImageName }}</p>
            </div>
            <div>
                当前图片确认为{{currentImageResultValue}}
            </div>
            <div class="button">
                <el-button type="primary" @click="submitResult" v-if="showButton">下一张</el-button>
                <div v-if="showMessage">当前版本{{formattedOriginalVersion}} - {{formattedCompareVersion}}的对比结果已全部查看</div>
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
    name: 'getResult',
    data() {
      return {
        images: [],
        currentImageIndex: 0,
        maxHeight: 0,
        showMessage: false,
        showButton: true,
        originalVersion: this.$route.params.originalVersion,
        compareVersion: this.$route.params.compareVersion,
        currentImageResultValue: '',
        };
    },
    mounted() {
      this.maxHeight = window.innerHeight - 200;
      axios.get(`/api/get_version_abnormal_images?originalVersion=${this.$route.params.originalVersion}&compareVersion=${this.$route.params.compareVersion}`)
      .then((response) => {
        this.images = response.data;
        console.log(this.images);
        this.getCurrentImageResult();
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
      async currentImageResult() {
        try {
          if (this.images && this.images.length && this.images[this.currentImageIndex]) {
            let con_data = {                
              image_version_ori: this.$route.params.originalVersion,
              image_version_tar: this.$route.params.compareVersion,
              image_name: this.images[this.currentImageIndex].name,
            }
            let response = await axios.post('/webapi/get_confirm', con_data);
            console.log(response.data);
            let r = response.data;
            if (r === 1) {
              console.log(r);
              return '正常外观';
            } else {
              console.log(r);
              return '异常外观';
            }
          } else {
            return '';
          }
        } catch (error) {
          console.error(error.response.data);
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
        if (this.currentImageIndex < this.images.length - 1) {
          this.currentImageIndex++;
          this.getCurrentImageResult(); 
        }else {
          this.showButton = false;
          this.showMessage = true;
        }
        this.result = null;
      },
      async getCurrentImageResult() { 
        // 获取当前图片的确认结果，并将其保存在 currentImageResultValue 属性中 
        this.currentImageResultValue = await this.currentImageResult; 
      }, 
      goBack() {
        console.log('go back');
        this.$router.push('/');
      }
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