<template>
<div class="home">
  <el-container>
    <el-table
      :data="unconfirmedVersions"
      stripe="true"
      style="width: 100%"
      height="400">
      <el-table-column
        prop="oriinfo"
        label="基准版本号"
        width="400">
      </el-table-column>
      <el-table-column
        prop="tarinfo"
        label="对比版本号"
        width="400">
      </el-table-column>
      <el-table-column
        prop="num"
        label="待确认图片数量">
      </el-table-column>
      <el-table-column
        prop="count"
        label="本次对比图片总数">
      </el-table-column>
      <el-table-column
        prop="imgtype"
        label="本次对比图片类型"
        width="400">
      </el-table-column>
      <el-table-column
      fixed="right"
      label="操作"
      width="200">
      <template slot-scope="scope">
        <el-button class="custom-button" @click="goConfirmVersion(scope.row)" type="text" size="small">前往确认</el-button>
      </template>
    </el-table-column>
    </el-table>
  </el-container>
  <el-container>
    <el-table
      :data="confirmedVersions"
      stripe="true"
      style="width: 100%"
      height="400">
      <el-table-column
        prop="oriinfo"
        label="基准版本号"
        width="400">
      </el-table-column>
      <el-table-column
        prop="tarinfo"
        label="对比版本号"
        width="400">
      </el-table-column>
      <el-table-column
        prop="num"
        label="已确认图片数量">
      </el-table-column>
      <el-table-column
        prop="count"
        label="本次对比图片总数">
      </el-table-column>
      <el-table-column
        prop="imgtype"
        label="本次对比图片类型"
        width="400">
      </el-table-column>
      <el-table-column
      fixed="right"
      label="操作"
      width="200">
      <template slot-scope="scope">
        <el-button class="custom-button" @click="viewResult(scope.row)" type="text" size="small">查看</el-button>
        <el-button class="custom-button" @click="goConfirmVersion(scope.row)" type="text" size="small">重新确认</el-button>
      </template>
    </el-table-column>
    </el-table>
  </el-container>
</div>
</template>
<script>
import axios from 'axios';

export default {
    name: 'Home',
    data() {
        return {
        unconfirmedVersions: [],
        confirmedVersions: []
        }
    },
    created() {
        this.getUnconfirmedVersions();
        this.getConfirmedVersions();
    },
    methods: {
        getUnconfirmedVersions() {
            axios.get('/webapi/get_unconfirm_version')
            .then(response => {
                console.log(response.data);
                this.unconfirmedVersions = response.data;
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
        getConfirmedVersions() {
            axios.get('/webapi/get_confirmed_version')
            .then(response => {
                console.log(response.data);
                this.confirmedVersions = response.data;
            })
            .catch(error => {
                console.log(error.response.data);
            })
            },
        goConfirmVersion(row) {
            // do something after row
            console.log(row);
            const tarinfo = row.tarinfo;
            const oriinfo = row.oriinfo;
            const tarinfoValue = tarinfo.split(' [')[0].trim();
            const oriinfoValue = oriinfo.split(' [')[0].trim();
            // console.log(tarinfoValue);
            // console.log(oriinfoValue);
            this.$router.push({ name: 'setResult', params: { originalVersion: oriinfoValue, compareVersion: tarinfoValue } })
        },
        viewResult(row) {
            // do something after row
            // console.log(row);
            const tarinfo = row.tarinfo;
            const oriinfo = row.oriinfo;
            const tarinfoValue = tarinfo.split(' [')[0].trim();
            const oriinfoValue = oriinfo.split(' [')[0].trim();
            this.$router.push({ name: 'getResult', params: { originalVersion: oriinfoValue, compareVersion: tarinfoValue } })
        }
    }
}
</script>
<style>
.el-table-column .cell.label {
    font-weight: bold; /* 加粗 */
}
.el-table-column .cell {
    color: #000000; /* 颜色 */
}
.custom-button {
  background-color: #409EFF;
  border-color: #409EFF;
  color: #fff;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.custom-button:hover {
  background-color: #66B1FF;
  border-color: #66B1FF;
}

</style>