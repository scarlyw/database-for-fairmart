<template>
  <div id="goodDetail">
    <Header> </Header>
    <div id="cai_good_detail">
      <ul id="caimenu">
        <!-- 这四个超链接暂时先这样凑活一下，以后要改 -->
        <!-- 鼠标进入时会改变颜色 -->
        <li
          id="caimenu_sy"
          @mouseover="gd_changeBcolor($event, '#a2a19f')"
          @mouseleave="gd_changeBcolor($event, '#E8E7E3')"
          @click="gotoHome"
        >
          <a title="首页"> 首页 </a>
        </li>
        <li
          id="caimenu_sc"
          @mouseover="gd_changeBcolor($event, '#a2a19f')"
          @mouseleave="gd_changeBcolor($event, '#E8E7E3')"
          @click="gotoHome"
        >
          <a title="商城"> 商城 </a>
        </li>
        <li
          id="caimenu_qg"
          @mouseover="gd_changeBcolor($event, '#a2a19f')"
          @mouseleave="gd_changeBcolor($event, '#E8E7E3')"
          @click="gotoSeek"
        >
          <a title="求购"> 求购 </a>
        </li>
        <li
          id="caimenu_lxwm"
          @mouseover="gd_changeBcolor($event, '#a2a19f')"
          @mouseleave="gd_changeBcolor($event, '#E8E7E3')"
        >
          <a href="https://github.com/scarlyw/database-for-fairmart" title="联系我们"> 联系我们</a>
        </li>
      </ul>
    </div>

    <div id="cai_detail_box">
      <div style="height: 640px">
        <!-- 这里放商品详情框上面的部分 -->
        <div style="width: 0px; height: 0px">
          {{ getDetail() }}
        </div>
        <div style="width: 684px; height: 464px; float: left">
          <img
            :src="photo"
            width="684px"
            height="464px"
            id="image"
          /><img />
        </div>
        <div
          style="
            width: 386px;
            height: 71px;
            margin-left: 64px;
            font-size: 48px;
            float: left;
          "
        >
          {{ this.title }}
        </div>
        <!--<div
          style="
            width: 299px;
            height: 30px;
            margin-left: 66px;
            font-size: 20px;
            color: red;
            float: left;
          "
        >
          {{ description }}
        </div>-->
        <div
          style="
            width: 412px;
            height: 71px;
            margin-left: 64px;
            font-size: 48px;
            float: left;
          "
        >
          <p style="margin: 0px; padding: 0px; color: gray; float: left">
            价格
          </p>
          <p style="margin: 0px; padding: 0px; color: red; float: right">
            ￥{{ price }}
          </p>
        </div>

        <!-- 画一条横线 -->
        <div style="height: 10px; width: 499px; margin-left: 42px; float: left">
          <hr />
        </div>
        <div
          style="
            width: 216px;
            height: 106px;
            margin-left: 41px;
            margin-top: 59px;
            float: left;
            font-size: 36px;
            color: rgba(181, 161, 161, 1);
          "
        >
          方便交易时间<br />
          全天
        </div>
        <!-- 画一条竖线 -->
        <div
          style="
            width: 10px;
            height: 176px;
            margin-left: 35px;
            margin-top: 24px;
            float: left;
            border-left: 1px solid rgba(166, 166, 166, 1);
          "
        ></div>
        <div
          style="
            width: 216px;
            height: 106px;
            margin-left: 25px;
            margin-top: 59px;
            float: left;
            font-size: 36px;
            color: rgba(181, 161, 161, 1);
          "
        >
          剩余有效期<br />
          30天
        </div>
        <!-- 画一条横线 -->
        <div
          style="
            height: 10px;
            width: 499px;
            margin-left: 42px;
            margin-top: 31px;
            float: left;
          "
        >
          <hr />
        </div>

        <!-- 下面还有两个按钮 -->
        <div
          style="
            height: 90px;
            width: 535px;
            margin-left: 42px;
            margin-top: 42px;
            float: left;
          "
        >
          <button
            type="button"
            style="
              height: 90px;
              width: 170px;
              float: left;
              font-size:35px;
              background-color: rgba(255, 77, 79, 1);
              border-radius: 15px;
              color: white;
            "
            @click="dialog_buying_Visible=true"
            v-if="display_buy_button"
          >
            立即购买
          </button>
          <button
            type="button"
            style="
              height: 90px;
              width: 170px;
              float: left;
              font-size: 35px;
              background-color: rgba(255, 77, 79, 1);
              border-radius: 15px;
              color: white;
            "
            @click="get_user_info"
            v-if="display_email_button"
          >
            联系卖家
          </button>
          <button
            type="button"
            style="
              height: 90px;
              width: 170px;
              margin-left: 20px;
              float: left;
              font-size: 35px;
              background-color: rgba(232, 169, 132, 1);
              border-radius: 15px;
              color: white;
            "
            @click="addtoFavorite"
            v-if="display_fav_button"
          >
            {{favorite_str}}
          </button>
        </div>
      </div>

      <div>
        <!-- 这里放 商品详情 文字部分 -->
        <!-- 字体什么的，以后再管了 -->
        <div
          style="
            height: 119px;
            width: 100%;
            float: left;
            background-color: rgba(196, 196, 196, 1);
          "
        >
          <p
            style="
              margin: 0px 0px 0px 35px;
              padding: 0px;
              color: white;
              float: left;
              font-size: 48px;
              line-height: 119px;
            "
          >
            商品详情
          </p>
        </div>
        <div style="min-height: 118px; width: 100%; float: left">
          <p
            style="
              margin: 10px 0px 0px 41px;
              padding: 0px;
              float: left;
              font-size: 36px;
              text-align: left;
              color: rgba(120, 66, 66, 1);
            "
          >
            {{this.description}}
          </p>
        </div>
        

          <el-dialog
            :visible.sync="dialog_buying_Visible"
            width="50%"
            style="text-align: center"
            :before-close="handleClose"
          >
            <!-- <repassword></repassword> -->
            <span>确认购买</span>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialog_buying_Visible = false">取 消</el-button>
              <el-button type="primary" @click="buyProduct"
                >确 定</el-button
              >
            </span>
          </el-dialog>

          <el-dialog
            :visible.sync="dialog_email_Visible"
            width="50%"
            style="text-align: center"
            :before-close="handleClose"
          >
            <!-- <repassword></repassword> -->
            <div>卖家邮箱：{{seller_email}}</div>
            <div>卖家其他联系方式：{{seller_contact_description}}</div>
            <span slot="footer" class="dialog-footer">
              <el-button type="primary" @click="dialog_email_Visible = false"
                >确 定</el-button>
            </span>
          </el-dialog>
        
      </div>
    </div>
    <!--<div style="float: right">
      <myInfirmation> </myInfirmation>
    </div>-->
  </div>
</template>

<script>
import myHeader from "@/components/myHeader";
import LeftSidebar from "@/components/LeftSidebar";
import DisplaySix from "@/components/DisplaySix";
import information from "@/components/myInformation";
import "element-ui/lib/theme-chalk/index.css";
import _first from "@/components/cai_msg";
import axios from "axios";
import GLOBAL from '@/global/global'

export default {
  name: "goodDetail",
  data() {
    return {
		//product_id:this.goodsContent.product_id,
      //title: this.goodsContent.product_name,
	  title: this.title,
      description: "",
      price: 0,
      seller_email:"",
      seller_contact_description:"",
      photo:"",
      product_id: this.$route.query.product_id,
      type:this.$route.query.type,
      dialog_buying_Visible: false,
      dialog_email_Visible: false,
      checkbuy:"",
      display_buy_button:true,
      display_fav_button:true,
      display_email_button:true,
      favorite_str:"加入收藏",
    };
  },
  created(){
    console.log(this.product_id);
    console.log("进入详情页面");
    console.log(this.type);
    this.selectToHide();
  },
  components: {
    Header: myHeader,
    myLeftSidebar: LeftSidebar,
    myDisplay: DisplaySix,
    myInfirmation: information,
    dongtai: _first,
  },
  methods: {
	  gotoHome()
	  {
	    this.$router.replace('/')
	  },
    gotoSeek(){
      this.$router.replace("/seekGoods")
    },
    selectToHide(){
      if(this.type==""){

      }else if(this.type==""){
        
      }else if(this.type==""){

      }
    },
    gd_changeBcolor(x, color) {
      x.currentTarget.style.background = color;
    },
    decodePhoto(data_str){
      var str=data_str;
      var data_start=str.indexOf("/9j")
      var data=str.slice(data_start,)
      var item_start=str.indexOf("/");
      var item_end=str.indexOf("base64")
      var item=str.slice(item_start+1,item_end);  
      data="data:image/"+item+";base64,"+data;
      
      console.log(data);
    },
    get_user_info() {
      if(GLOBAL.currentUser_ID=="")
      {
        alert("目前尚未登陆，请登录后再进行操作!");
        return;
      }
      this.dialog_email_Visible=true;
      if(this.seller_email == "") {
        var that = this;
        const seller_info_path = "http://localhost:8081/get_seller_info";
        var goodsInformation = {
          product_id: this.$route.query.product_id,
        };
        axios
          .post(seller_info_path,JSON.stringify(goodsInformation))
          .then(function (res) {
            var info = res.data;
            that.seller_email = info["email"];
            that.seller_contact_description = info["other_connect_description"];
          });
      }
    },
    getDetail() {
      console.log("!!!!!!1");
      //在这里传给后端
      var that = this;
      const path = "http://localhost:8081/product_info"; // 我也不知道
      var goodsInformation = {
        product_id: this.$route.query.product_id,
      };
      axios
        .post(path, JSON.stringify(goodsInformation))
        .then(function (response) {
          // response.setContentType("text/javascript;charset=UTF-8");
          var goods = response.data;
          console.log("!!!!!!!!!!!!!!!!" + goods["product_name"]);
          console.log(goods["product_id"]);
          console.log(goods["price"]);
          console.log(goods["state"]);
          console.log(goods["put_timestamp"]);
          // modified by xcc 2021.11.24 21:57
          that.title = goods["product_name"];
          that.description = goods["product_description"];
          that.price = goods["price"];
          that.photo = goods["photo"];
          //that.decodePhoto(goods["photo"]);
        });

        const favorite_path = "http://localhost:8081/get_favorite_state";
        var info = {
          product_id: this.$route.query.product_id,
          user_id: GLOBAL.currentUser_ID,
        };
        axios
          .post(favorite_path,JSON.stringify(info))
          .then(function (res) {
            var result = res.data;
            console.log(result);
            var is_exist = result.state;
            if(is_exist == true) {
              that.favorite_str = "已收藏";
            }
          });

    },
    handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      },
    handleConfirm(){
      console.log(this.checkbuy);
      this.dialog_buying_Visible=false;
    },
    buyProduct() {
      //如果没有登陆的话.....currentUser_id究竟是undefined还是空串呢
      if(GLOBAL.currentUser_ID=="")
      {
        alert("目前尚未登陆，请登录后再进行操作!");
        return;
      }

      //获取商品和买家信息
      const  path="http://localhost:8081/buy_product";
      var buyEvent={
        "user_id":GLOBAL.currentUser_ID,
        "product_id":this.product_id,
      }
      var that=this;
      //此处打印很成功，注意键值对的格式
      console.log(buyEvent);

      axios
					.post(path,JSON.stringify(buyEvent))
					.then(function(response){
						var buy_result=response.data
						var  result = buy_result["result"];
            var is_buy_success = buy_result["state"]
						//alart(is_register_success)
						console.log(buy_result);//注意返回格式
						if(is_buy_success == false&&result==="outOfMoney"){
							alert("余额不足，请充值");
              that.dialog_buying_Visible=false;
						}
            else if(is_buy_success == false&&result==="sold") {
							alert("商品已售出");
              that.dialog_buying_Visible=false;
            }
            else if(is_buy_success == true){
              var alert_str="购买成功"
              that.dialog_buying_Visible=false;
							alert(alert_str);
              
						}else{
							alert("买了个什么玩意？");
						}
					});
    },
    //根据type确定每个组件是否进行显示
    handleDisplay(){

    },
    addtoFavorite(){
      var that = this;
      if(GLOBAL.currentUser_ID==""){
        alert("请登录后重试");
        return;
      }
      if(this.favorite_str == "已收藏") {
        console.log("进入删除收藏函数")
        const path="http://localhost:8081/delete_favorite"
        var favorite_info={
          "user_id":GLOBAL.currentUser_ID,
          "product_id":this.product_id
        }
        axios
            .post(path,JSON.stringify(favorite_info))
            .then(function(response){
              var favorite_result=response.data
              var delete_favorite_success = favorite_result["state"];
              //alart(is_register_success)
              console.log(favorite_result);//注意返回格式
              if(delete_favorite_success===true){
                that.favorite_str = "加入收藏";
                alert("已取消收藏");
              }else{
                var alert_str="取消收藏失败";
                alert(alert_str);
                }

            });
      }
      else {
        console.log("进入收藏函数")
        const path="http://localhost:8081/add_favorite"
        var favorite_info={
          "user_id":GLOBAL.currentUser_ID,
          "product_id":this.product_id
        }
        axios
            .post(path,JSON.stringify(favorite_info))
            .then(function(response){
              var favorite_result=response.data
              var  is_favorite_success = favorite_result["state"];
              //alart(is_register_success)
              console.log(favorite_result);//注意返回格式
              if(is_favorite_success===true){
                that.favorite_str = "已收藏";
                alert("收藏成功");
              }else{
                var alert_str="收藏失败"
                alert(alert_str);
                }

            });
      }
    }
  },
  
  props: ["goodId"],
};
</script>

<style>
#goodDetail {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  margin-right: 0px;
  float: center;
  margin: auto;
}

#cai_good_detail {
  height: 48px;
  width: 1120px;
  padding-top: 0px;
  margin-left: 200px;
  
  border: 0px;
  background: #e8e7e3;
}

#caimenu {
  padding: 0px;
  position: relative;
  text-align: center;
}

#caimenu_sy {
  height: 48px;
  width: 280px;
  list-style: none;
  float: left;
  font-size: 30px;
}

#caimenu_sc {
  height: 48px;
  width: 280px;
  list-style: none;
  float: left;
  font-size: 30px;
}

#caimenu_qg {
  height: 48px;
  width: 280px;
  list-style: none;
  float: left;
  font-size: 30px;
}

#caimenu_lxwm {
  height: 48px;
  width: 280px;
  list-style: none;
  float: left;
  font-size: 30px;
}

#cai_detail_box {
  width: 1261px;
  /*min-height: 880px;*/
  margin-left: 120px;
  margin-top: 30px;
  float: left;
}
#demo {
  width: 100px;
  height: 100px;
  background-color: blue;
}
</style>
