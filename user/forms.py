from django import forms
from django.contrib.auth import password_validation
from django.core.validators import validate_email, MinLengthValidator
from .models import User


class EmailConfirmationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )


    def save(self, commit=True):
        user = super().save(commit)
        user.save()

        return user


class CodeVerifyForm(forms.Form):
    code = forms.CharField(max_length=4)


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'style': 'width: 300px;', 'class': 'form-control'}),
        required=True  # Make the email field required
    )

class SetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'style': 'width: 300px;', 'class': 'form-control'}),
        required=True  # Make the email field required
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True  # Make the password field required
    )

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=User._meta.get_field('username').max_length,
        error_messages={
            'required': 'Username is required.',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'profile_pic']




class ChangePassForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

