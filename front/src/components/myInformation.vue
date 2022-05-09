<!-- right side,for my information and menu -->
<template>
  <div class="information" id="bgr">
    <div>
      <img
        src="../assets/logo.jpg"
        width="200"
        height="150"
        id="image"
        @click="gotoGerenzhuye"
        border-radius="10xp"
      /><img />
      <el-col :span="24" id="item">
        <span style="font-size:30px">{{userName}}</span>
        <el-menu
          default-active="0"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          background-color="#696969"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
        <div style="font-size:15px; margin:10px; color:#ffffff">邮箱：{{email}}</div>
        <div style="font-size:15px;color:#ffffff">账户余额：{{money}}</div>
          <!-- <el-menu-item index="1" class="Item">
            <i class="el-icon-message"></i>
            <span style="font-size:18px">我的消息</span>
          </el-menu-item> -->

          <el-menu-item index="2" class="Item">
            <i class="el-icon-shopping-cart-2"></i>
            <span slot="title" style="font-size:18px" @click="gotoMyPurchase"> 购买记录</span>
          </el-menu-item>

          <el-menu-item index="3" class="Item">
            <i class="el-icon-star-on"></i>
            <span slot="title" style="font-size:18px" @click="gotoMyFavorite">收藏夹</span>
          </el-menu-item>

          <el-menu-item index="4" class="Item">
            <i class="el-icon-upload"></i>
            <span slot="title" style="font-size:18px" @click="gotoCreate">发布商品</span>
          </el-menu-item>

          <!-- <el-menu-item index="5" class="Item">
            <i class="el-icon-upload2"></i>
            <span slot="title" style="font-size:18px" @click="gotoPut">发布求购</span>
          </el-menu-item>

          <el-menu-item index="5" class="Item">
            <i class="el-icon-view"></i>
            <span slot="title" style="font-size:18px" @click="gotoSeek">浏览求购</span>
          </el-menu-item> -->

        </el-menu>
      </el-col>
    </div>
  </div>
</template>

<script>
import GLOBAL from '@/global/global'
export default {
  inject:["reload"],
  data(){
    return{
      userName:GLOBAL.currentUser_name,
      money:GLOBAL.money,
      email:GLOBAL.email,
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    gotoCreate(){
      this.$router.replace('/createItem')
    },
    gotoMyPurchase(){
      this.$router.push({path:"/myGoods",query: {type:"my_purchase"}});
    },
    gotoGerenzhuye()
    {
      this.$router.replace('/gerenzhuye')
    },
    gotoSeek(){
      this.$router.replace('/seekGoods')
    },
    gotoPut(){
      this.$router.replace('/putGoods')
    },
    gotoMyFavorite(){
      this.$router.push({path:"/myGoods",query: {type:"my_favorites"}});
    }
  },
  watch :{
        '$router': function (to, from) {
          this.reload();
        }
  },
};
</script>

<style>
#bgr {
  width: 280px;
  float: left;
  margin-top: 30px;
  /*margin-right: 2%;*/
  position: relative;
  /*right:-200px;*/
	margin-left: auto;
  margin-right : 20px;
  border-radius: 25px;
  background: #696969;
  display: flex;
  height: 600px;
	
}
#id {
  widows: 317px;
}
#image {
  margin: 30px;
}
.Item{
  margin:10px;
}
</style>