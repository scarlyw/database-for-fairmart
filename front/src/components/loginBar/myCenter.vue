<!-- 将原来右侧的个人信息已到右上角的边栏，伴随调整myHeader的高度 -->
<template>
  <div>
    <span class="mycenter">
      <span id="navi-menu">
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
        >
          <el-menu-item index="1" @click="dialog_deposit_Visible=true">充值</el-menu-item>
          <el-submenu index="2">
            <template slot="title">我的商品</template>
            <el-menu-item index="2-1" @click="gotoMyGoods"
              >我发布的</el-menu-item
            >
            <el-menu-item index="2-2" @click="gotoMyPurchase">我拍下的</el-menu-item>
            <el-menu-item index="2-3" @click="gotoMyFavorite">我的收藏</el-menu-item>
          </el-submenu>
          <el-menu-item index="3" @click="dialog_changecontact_Visible=true">更改联系方式</el-menu-item>
          <el-menu-item index="4" style="margin=0px;"
            ><a target="_blank" @click="quit"
              >退出登录</a
            ></el-menu-item
          >
        </el-menu>
      </span>
    </span>
    <el-dialog
      :visible.sync="dialog_changecontact_Visible"
      width="50%"
      style="text-align: center"
      
    >
      <div>您当前的联系信息：{{currentContact}}</div>
      <span>请输入您的联系方式信息</span>
      <el-input v-model="myContact"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog_changecontact_Visible = false">取 消</el-button>
        <el-button type="primary" @click="changeContact">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      :visible.sync="dialog_deposit_Visible"
      width="50%"
      style="text-align: center"
      
    >
      <span>请输入充值金额</span>
      <el-input v-model="myDeposit"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog_deposit_Visible = false">取 消</el-button>
        <el-button type="primary" @click="deposit">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import GLOBAL from "@/global/global";
import axios from "axios";
import Router from "../../router/index.js";
export default {
  data() {
    return {
      myContact:"",
      dialog_changecontact_Visible: false,
      currentContact:GLOBAL.contact_description,
      dialog_deposit_Visible: false,
      myDeposit:"",
    };
  },

  components: {},

  computed: {},

  mounted: {},

  methods: {
    gotoMyGoods() {
        Router.push({ path: '/myGoods', query: { type: "user_all_products" }});
    },
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
    gotoMyPurchase(){
      console.log("goto my churse");
      Router.push({path:"/myGoods",query: {type:"my_purchase"}});
    },
    gotoMyFavorite(){
      console.log("goto my favorite");
      Router.push({path:"/myGoods",query: {type:"my_favorites"}});
    },
    quit(){
      this.$router.go(0);

    },
    changeContact() {
      if(GLOBAL.currentUser_ID == "") {
        dialog_changecontact_Visible = false;
        alert("请登录后再试");
      }
      const path = "http://localhost:8081/change_contact_info";
      var that = this;
      var Info = {
        user_id: GLOBAL.currentUser_ID,
        other_contact_info: this.myContact,
      };
      axios.post(path, JSON.stringify(Info)).then(function (response) {
        console.log("accept");
        var result = response.data;
        var change_success = result["state"];
        if (change_success == true) {
          GLOBAL.contact_description = that.myContact;
          that.currentContact = that.myContact;
          that.dialog_changecontact_Visible = false;
          that.myContact = "";
        } else {
          alert("修改失败，请重试");
        }
      });
    },
    deposit() {
      var that = this;
      const path = "http://localhost:8081/deposit";
      if(GLOBAL.currentUser_ID == "") {
        dialog_changecontact_Visible = false;
        alert("请登录后再试");
      }
      var depositMoney = Number(this.myDeposit,10);
      if(isNaN(depositMoney)) {
        alert("请输入数字");
        myDeposit = "";
      }
      else if(depositMoney <= 0) {
        alert("请输入大于0的充值金额");
        myDeposit = "";
      }
      var Info = {
        user_id: GLOBAL.currentUser_ID,
        money: this.myDeposit,
      };
      axios.post(path, JSON.stringify(Info)).then(function (response) {
        console.log("accept");
        var result = response.data;
        var deposit_success = result["state"];
        if (deposit_success == true) {
          GLOBAL.money = Number(GLOBAL.money,10)+depositMoney;
          that.dialog_deposit_Visible = false;
          that.myDeposit = "";
          Router.push("/");
        } else {
          alert("充值失败，请重试");
        }
      });
    },
  },
};
</script>

<style>
.mycenter {
  float: right;
  margin: auto;
  height: 70px;
}
#myphoto {
  margin: auto;
  width: 70px;
  height: 70px;
  float: left;
}
#navi-menu {
  width: 500px;
  float: left;
}
</style>