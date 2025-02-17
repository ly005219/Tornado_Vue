<template>
  <div>
    <div class="modify_content">
      <form>
        <input type="hidden" name="_id" :value="user.id" ref="modify_item_id" />
        <input
          type="hidden"
          name="password"
          :value="user.password"
          ref="modify_item_pwd"
        />
        <div class="modify_item1">
          <label for>账号：</label>
          <div ref="modify_item_email" class="modify_item_email">
            {{ user.email }}
          </div>
        </div>
        <div class="modify_item2">
          <label for>昵称：</label>
          <input
            ref="modify_item_nickname"
            type="text"
            name="nick_name"
            id="nickname"
            :value="user.nick_name"
          />
        </div>
        <div class="modify_item3">
          <label class="modify_item3_label">性别：</label>
          <div class="modify_item_gender">
            <label>
              <input
                type="radio"
                :checked="gender_1"
                name="gender"
                value="1"
              />男
            </label>
            <label>
              <input
                type="radio"
                :checked="gender_2"
                name="gender"
                value="2"
              />女
            </label>
            <label>
              <input
                type="radio"
                :checked="gender_3"
                name="gender"
                value="0"
              />保密
            </label>
          </div>
        </div>
        <div class="modify_item4">
          <label for>签名：</label>
          <textarea
            ref="modify_item_signatrue"
            name="signatrue"
            id="bio"
            cols="30"
            rows="10"
            :value="user.signatrue"
          ></textarea>
        </div>
        <div class="modify_item5">
          <label for>头像：</label>
          <img
            v-if="user != ''"
            :src="'http://localhost:8000' + user.pic"
            alt
            ref="pic_img"
            class="avatar"
          />
          <img v-if="user == ''" src="@/assets/img/avatar-default.png" alt />
          <input
            type="file"
            id="pic"
            ref="pic"
            @change="getFileContent()"
            name="pic"
            accept="image/*"
          />
        </div>
        <button type="button" @click="modifyBty" class="modify_btn">
          保存
        </button>
      </form>
    </div>
  </div>
</template>

<style lang="less">
.modify_content {
  width: 100%;
  .modify_item1 {
    width: 100%;
    height: 50px;
    background: white;
    label {
      display: block;
      float: left;
      width: 20%;
      height: 50px;
      line-height: 50px;
      text-align: center;
    }
    div {
      float: left;
      width: 75%;
      height: 50px;
      line-height: 50px;
      text-align: right;
    }
  }
  .modify_item2 {
    width: 100%;
    height: 50px;
    background: white;
    label {
      display: block;
      float: left;
      width: 20%;
      height: 50px;
      line-height: 50px;
      text-align: center;
    }
    input {
      float: left;
      width: 75%;
      text-align: right;
    }
  }
  .modify_item3 {
    width: 100%;
    height: 50px;
    background: white;
    .modify_item3_label {
      display: block;
      float: left;
      width: 20%;
      height: 50px;
      line-height: 50px;
      text-align: center;
    }
    .modify_item_gender {
      float: left;
      width: 75%;
      height: 50px;
      text-align: center;
      line-height: 50px;
      display: flex;
      label {
        flex: 1;
      }
    }
  }
  .modify_item4 {
    width: 100%;
    height: 120px;
    background: white;
    label {
      display: block;
      float: left;
      width: 20%;
      height: 50px;
      line-height: 50px;
      text-align: center;
    }
    #bio {
      float: left;
      width: 75%;
      height: 100px;
    }
  }
  .modify_item5 {
    width: 100%;
    height: 100px;
    background: white;
    label {
      display: block;
      float: left;
      width: 20%;
      height: 50px;
      line-height: 50px;
      text-align: center;
    }
    img {
      width: 50px;
      height: 50px;
    }
  }
  .modify_btn {
    width: 100%;
    height: 50px;
    border-radius: 20px;
    color: white;
    font-size: 20px;
    background: red;
  }
}
</style>

<script>
import { Toast } from "mint-ui";
import myaxios, { getsessionURL, modifypersonURL } from "@/tools/myaxios.js";
import { EALREADY } from "constants";
import { read } from "fs";
import axios from "axios";
export default {
  data: function () {
    return {
      user: [],
      gender_1: false,
      gender_2: false,
      gender_3: false,
    };
  },
  methods: {
    getFileContent() {
      var reader = new FileReader();
      var files = this.$refs.pic.files;

      if (files && files.length > 0) {
        //读取pic文件域中的文件数据
        reader.readAsDataURL(files[0]);
        //当数据读取完毕的时候
        reader.onload = () => {
          //让图片预览中显示上传的图片信息
          this.$refs.pic_img.src = reader.result;
        };
      }
    },
    async modifyBty() {
      var id = this.$refs.modify_item_id.value;
      var email = this.$refs.modify_item_email.innerHTML;
      var nick_name = this.$refs.modify_item_nickname.value;
      var pwd = this.$refs.modify_item_pwd.value;
      var gender = document.querySelector(
        ".modify_item_gender label input:checked"
      ).value;
      var signatrue = this.$refs.modify_item_signatrue.value;
      var pic = this.$refs.pic.files[0];
      var params = new FormData();

      params.append("id",id);
      params.append("email",email);
      params.append("nick_name",nick_name);
      params.append("password",pwd);
      params.append("gender",gender);
      params.append("signatrue",signatrue);
      params.append("pic",pic);
      
      axios
        .post("/api/user/update", params, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((res) => {
          if (res.data.code == 200) {
            this.$router.go(-1);
            Toast(res.data.msg);
          }
        });
    },
  },
  async created() {
    var result = await myaxios("GET", getsessionURL);
    if (result.data.user) {
      this.user = result.data.user;
      if (this.user.gender == 1) {
        this.gender_1 = true;
      } else if (this.user.gender == 2) {
        this.gender_2 = true;
      } else {
        this.gender_3 = true;
      }
    }
  },
  mounted() {
    var header_title = document.getElementsByClassName("mint-header-title")[0];
    header_title.innerText = "修改信息";
  },
};
</script>