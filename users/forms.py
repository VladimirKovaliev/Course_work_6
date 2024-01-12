from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class EnterCodeForm(forms.Form):
    code = forms.CharField(label='код', max_length=4)


class SendPasswordForm(forms.Form):
    email = forms.EmailField(label='email', max_length=100)
