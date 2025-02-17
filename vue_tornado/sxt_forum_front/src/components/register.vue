<template>
  <div>
    <div class="mui-content">
      <form class="mui-input-group">
        <div class="mui-input-row">
          <label>邮箱</label>
          <input
            id="phone"
            ref="email"
            type="text"
            class="mint-field-core mui-input"
            placeholder="请输入账号"
          />
        </div>
        <div class="mui-input-row">
          <label>昵称</label>
          <input
            id="nickname"
            ref="nickname"
            type="text"
            class="mint-field-core mui-input"
            placeholder="请输入昵称"
          />
        </div>
        <div class="mui-input-row">
          <label>密码</label>
          <input
            id="password"
            ref="password"
            type="password"
            class="mint-field-core mui-input"
            placeholder="请输入密码"
          />
        </div>
     
        <div class="mui-input-row">
          <label>确认密码</label>
          <input
            id="password_confirm"
            ref="password2"
            type="password"
            class="mint-field-core"
            placeholder="请确认密码"
          />
        </div>
        <div class="mui-input-row mint-cell mint-field">
          <label>验证码</label>
          <input
            id="check_code"
            ref="check_code"
            type="text"
            class="mint-field-core"
            placeholder="请输入验证码"
          />
          
        </div>
         <button id="send_code" class="mui-btn mui-btn-warning mint-button--small mint-field-core" @click="send_code">发送验证码</button>
                <button id="reg" class="mint-button mint-button--primary mint-button--small  mint-field-core" @click="register">注册</button>
      </form>
    
 
   
    </div>
  </div>
</template>

<script>
import { Toast } from "mint-ui";
import myaxios, { registerURL,sendMsg } from "@/tools/myaxios.js";
import { EALREADY } from "constants";
export default {
  data: function() {
    return {};
  },
  methods: {
    async register() {
      var email = this.$refs.email.value;
      var nickname = this.$refs.nickname.value;
      var password = this.$refs.password.value;
      var password2 = this.$refs.password2.value;
      var check_code = this.$refs.check_code.value;
      if (!email) {
        Toast("请输入您的邮箱！");
        return;
      } else if (!password) {
        Toast("请输入您的密码！");
        return;
      } else if (!nickname) {
        Toast("请输入您的昵称！");
        return;
      } else if (!password) {
        Toast("请输入您的密码！");
        return;
      } else if (password != password2) {
        Toast("输入的两次密码不一致！");
        return;
      } else {
        var obj = {
            email: email,
            nick_name: nickname,
            password: this.$md5(password),
            code:check_code
          };
 
        var result = await myaxios("POST", registerURL, obj);
        if (result.data.code == 200) {
          console.log(result.data.msg)
          this.$router.push("/login");
        } else {
          Toast("账户已注册！");
        }
      }
    },
    async send_code(){
      var email = this.$refs.email.value;
      var obj = {email: email}
      result = await myaxios('POST',sendMsg,obj);
      if (result.data.code == 200){
        console.log(123)
      }
    }

  },
  mounted() {
    var header_title = document.getElementsByClassName("mint-header-title")[0];
    header_title.innerText = "注册";
  }
};
</script>