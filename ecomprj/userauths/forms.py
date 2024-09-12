from django import forms 
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User 

class UserRegisterForm(UserCreationForm) : 
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'الإسم'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder' : 'الإيميل'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'كلمة السر'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'تأكيد كلمة السر'}))

    class Meta : 
        model = User
        fields = ['username', 'email']