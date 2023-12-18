<template>
  <div id="app">
    <h2>命令行程序自动运行系统</h2>
    <el-container>
      <el-header>
        <el-menu mode="horizontal" router
        :default-active="$route.path">
          <el-menu-item index="/">
            <span>预设命令列表</span>
          </el-menu-item>
          <el-menu-item index="/record">
            <span>运行记录</span>
          </el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <!-- 在这里添加你的记账信息 -->
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
router-link{
  width:max-content;
  height: 60px;
}
</style>
