from .models import UserProfile
from  django import forms
from . import until
from . import errors
import os
class  RegisterForm(forms.ModelForm):
    ver_code = forms.CharField()
    password = forms.CharField(
        min_length=6,
        widget=forms.widgets.PasswordInput(render_value=True),
        max_length=20
    )
    class Meta:
        model = UserProfile
        fields = ('nick_name','phone')
    def __init__(self, *args, **kwargs):
        self.ver_path = kwargs.pop('ver_path', None)
        super(RegisterForm, self).__init__(*args, **kwargs)
        err_field = {
            'ver_code':'验证码',
            'password':'密码',
            'nick_name':'昵称',
            'phone':'手机号码'
        }
        for field in iter(self.fields):
            # self.fields[field].error_messages = {
            #     'required': '请输入'+ err_field[field]+'!'
            # }
            self.fields[field].required = False
            self.fields[field].widget.attrs.update({
                'class': 'input-text',
                'id':field
            })
    def clean_nick_name(self):
        data = self.cleaned_data.get('nick_name')
        # if until.name_filter(name):
        if len(data) == 0:
            raise  forms.ValidationError('昵称不能为空')
        try:
            until.name_filter(data)
        except errors.naneNullError:
            raise forms.ValidationError('昵称不能为空')
        except errors.lengthError as err:
            if err.code == 1001:
                raise forms.ValidationError('昵称长度不能超过15个字符！')
    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        err = until.phone_filter(data,UserProfile)
        if err is not None:
            raise forms.ValidationError(err)

    def clean_ver_code(self):
        data = self.cleaned_data.get('ver_code')
        err = until.check_verification(data,self.ver_path)
        if err is not None:
            raise forms.ValidationError(err)