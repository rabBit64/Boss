from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    
class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(label='이름', label_suffix='')
    last_name = forms.CharField(label='성', label_suffix='')
    email = forms.EmailField(label='이메일', label_suffix='')
    password = ReadOnlyPasswordHashField(
        label='',
        label_suffix='',
        help_text=_(
            '<a href="{}">비밀번호 변경하기</a>'
        ),
    )
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            'email',
            'first_name',
            'last_name',
        )