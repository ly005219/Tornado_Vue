from wtforms_tornado import Form
from wtforms import HiddenField
from wtforms.fields import StringField
from wtforms.validators import DataRequired,Length


class UserForm(Form):
    id = HiddenField()
    email = StringField('账号',validators=[DataRequired(message='请填写合法的邮箱地址'),Length(min=5,max=20,message='请输入5-10长度的昵称')])
    nick_name = StringField('昵称',validators=[Length(min=2,max=10,message='请输入2-10长度的昵称')])
    password = StringField('密码',validators=[Length(min=2,message='请输入2以上长度的密码')])
    signatrue = StringField('签名')
    pic = StringField('头像')


class LoginUserForm(Form):
    id = HiddenField()
    email = StringField('账号',validators=[DataRequired(message='请填写合法的邮箱地址'),Length(min=5,max=20,message='请输入5-10长度的昵称')])
    nick_name = StringField('昵称')
    password = StringField('密码',validators=[Length(min=2,message='请输入2以上长度的密码')])
    signatrue = StringField('签名')
    pic = StringField('头像')


class UpdateUserForm(Form):
    id = HiddenField()
    email = StringField('账号',validators=[DataRequired(message='请填写合法的邮箱地址'),Length(min=5,max=20,message='请输入5-10长度的昵称')])
    nick_name = StringField('昵称',validators=[Length(min=2,max=10,message='请输入2-10长度的昵称')])
    gender = StringField('性别')
    signatrue = StringField('签名')
    pic = StringField('头像')

class AddTopicForm(Form):
    type_ = StringField('类型',validators=[DataRequired(message='请选择类型')])
    title = StringField('标题',validators=[DataRequired(message='请填写标题')])
    content = StringField('内容')


