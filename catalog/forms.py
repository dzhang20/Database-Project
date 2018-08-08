from django import forms

class NewEventForm(forms.Form):
	title = forms.CharField(max_length=100)
	keyword = forms.CharField(max_length=100)
	address = forms.CharField(max_length=100)
	description = forms.CharField()

class SearchForm(forms.Form):
	title = forms.CharField(max_length=100)
	keyword = forms.CharField(max_length=100)
	address = forms.CharField(max_length=100)
	description = forms.CharField()
class LoginForm(forms.Form):
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)

# 引入验证码field
#from captcha.fields import CaptchaField

# 验证码form & 注册表单form
class RegisterForm(forms.Form):
    # 此处email与前端name需保持一致。
    email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)
