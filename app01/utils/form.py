from app01 import models
from django import forms
from django.core.exceptions import ValidationError
from app01.utils.encrypt import md5


class BootStrapModelForms(forms.ModelForm):
    bootstrap_class_exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label,
                    "autocomplete": "off"
                }


class UserModelForm(BootStrapModelForms):
    name = forms.CharField(min_length=3, max_length=10)

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyNumForm(BootStrapModelForms):
    class Meta:
        model = models.PrettyNumber
        # fields = ['mobile', 'price', 'level', 'status']
        fields = "__all__"

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        exists = models.PrettyNumber.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("号码已存在")
        return txt_mobile


class PrettyNumEditForm(BootStrapModelForms):
    mobile = forms.CharField(
        label="手机号",
        disabled=True,
    )

    class Meta:
        model = models.PrettyNumber
        fields = "__all__"


class AdminModelForm(BootStrapModelForms):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = '__all__'
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_username(self):
        txt_username = self.cleaned_data["username"]
        exists = models.Admin.objects.filter(username=txt_username).exists()
        if exists:
            raise ValidationError("用户名重复")
        return txt_username

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


class AdminModelEditForm(BootStrapModelForms):
    class Meta:
        model = models.Admin
        fields = ["username"]

    def clean_username(self):
        txt_username = self.cleaned_data["username"]
        exists = models.Admin.objects.filter(username=txt_username).exists()
        if exists:
            raise ValidationError("用户名重复")
        return txt_username


class AdminModelResetForm(BootStrapModelForms):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_password = md5(pwd)

        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_password).exists()
        if exists:
            raise ValidationError("密码不能与上次一致")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


class AccountModelForm(BootStrapModelForms):
    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    # def clean_password(self):
    #     pwd = self.cleaned_data.get("password")
    #     return md5(pwd)


class AssetsModelForm(BootStrapModelForms):
    bootstrap_class_exclude = ['app']

    class Meta:
        model = models.AssetsInfo
        fields = "__all__"
        widgets = {
            # "app": forms.CheckboxSelectMultiple(attrs={'class': 'form-check'})
            "app": forms.CheckboxSelectMultiple
        }


class PasswordManagementModelForm(BootStrapModelForms):
    class Meta:
        model = models.PasswordManagement
        # exclude = ["url"]
        # fields = ["url", "username", "remark"]
        fields = "__all__"

    def clean_url(self):
        txt_url = self.cleaned_data["url"]
        exists = models.PasswordManagement.objects.filter(url=txt_url).exists()
        if exists:
            raise ValidationError("已存在的记录")
        return txt_url


class PasswordManagementEditModelForm(BootStrapModelForms):
    class Meta:
        model = models.PasswordManagement
        exclude = ["url"]


class PasswordManagementRecordModelForm(BootStrapModelForms):
    class Meta:
        model = models.PasswordManagementRecord
        fields = "__all__"


class AppModelForm(BootStrapModelForms):
    class Meta:
        model = models.Application
        fields = "__all__"


class AppEditModelForm(BootStrapModelForms):
    class Meta:
        model = models.Application
        fields = ["app_name"]

    def clean_app_name(self):
        txt_app_name = self.cleaned_data["app_name"]
        exists = models.Application.objects.filter(app_name=txt_app_name).exists()
        if exists:
            raise ValidationError("记录重复")
        return txt_app_name


class LowValueConsumableModelForm(BootStrapModelForms):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
                field.widget.attrs["readonly"] = "readonly"
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label,
                    "autocomplete": "off",
                }

    class Meta:
        model = models.LowValueConsumable
        fields = "__all__"


class LowValueConsumableEditModelForm(BootStrapModelForms):
    class Meta:
        model = models.LowValueConsumable
        fields = "__all__"


class LowValueConsumableRecordModelForm(BootStrapModelForms):
    class Meta:
        model = models.LowValueConsumableRecord
        fields = "__all__"
