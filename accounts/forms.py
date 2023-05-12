from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, AuthenticationForm
from django.utils.translation import gettext_lazy as _



# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(
#         label='',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': '아이디 입력',
#                 'style': 'width: 360px; height: 40px;',
                
#             }))

#     password = forms.CharField(
#         label='',
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': '비밀번호 입력',
#                 'style': 'width: 360px; height: 40px;',
#             }))
    

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='사용자 이름', 
        widget=forms.TextInput(
            attrs={
                'autofocus': True, 
                'class': 'form-control',
                'style': 'width: 360px; height: 40px;',
                }))

    password = forms.CharField(
        label='비밀번호', 
        strip=False, 
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password', 
                'class': 'form-control',
                'style': 'width: 360px; height: 40px;',
                }))





class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='아이디', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width: 360px;','placeholder': '아이디 (2~15자)','id':'user_id',}))
    
    email = forms.EmailField(label='이메일', label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'style': 'width: 360px;', 'placeholder': '이메일',}))
    
    first_name = forms.CharField(label='성', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 180px;', 'placeholder': '성',}))
    
    last_name = forms.CharField(label='이름', label_suffix='', widget=forms.TextInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 180px;', 'placeholder': '이름',}))

    password1 = forms.CharField(label='비밀번호', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control placeholder-font','style': 'width: 360px;', 'placeholder': '비밀번호',}))
    
    password2 = forms.CharField(label='비밀번호 확인', label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'form-control placeholder-font', 'style': 'width: 360px;','placeholder': '비밀번호 확인',}))

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