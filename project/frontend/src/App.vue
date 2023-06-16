<template>
    <el-container>
    <el-header class="my-header"> L32时装对比 </el-header> 
    <el-main>
        <router-view />
    </el-main>
    </el-container>
</template>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}

#nav {
    padding: 30px;
}

#nav a {
    font-weight: bold;
    color: #2c3e50;
}

#nav a.router-link-exact-active {
    color: #42b983;
}

.my-header {
    background-color: #409EFF; /* 背景色 */
    color: #FFFFFF; /* 字体颜色 */
    font-size: 24px;
    height: 80px; /* 元素高度 */
    line-height: 60px; /* 竖向居中 */
}

</style>