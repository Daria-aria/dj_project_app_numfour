from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from django import forms
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget, NumberInput
from django.forms.fields import EmailField
from django.forms.forms import Form
from .models import *

REG_CHOICES = [
    'I agree with Terms and Privacy policy',
    'I agree to receive marketing information'
]


class UserForm(UserCreationForm):
    username = forms.CharField(label='Login', max_length=50, min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', max_length=200, help_text='Required')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    # confirmation = forms.MultipleChoiceField(required=False, label='Confirm options', widget=forms.CheckboxSelectMultiple(), choices=REG_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError('Login already exists. Please choose another login.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError('Email already exists. Cannot register new user with this email.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError('Password does not match')
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        if commit:
            user.save()
        return user


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField(label='', help_text='Fill in letters from the pic')


class UserUpdForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdForm(forms.ModelForm):
    CHOICES=[('writer', 'Writer'), ('follower', 'Follower'), ('critic', 'Critic'),]
    userpic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                          empty_value='the user prefers not to share his/her bio information.')
    user_name = forms.CharField()
    date_of_birth = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    statusType = forms.ChoiceField(choices=CHOICES)
    friends = forms.CharField()
    followers = forms.CharField()

    class Meta:
        model = Profile
        fields = ['userpic', 'user_name', 'date_of_birth', 'statusType', 'bio', 'friends', 'followers']

#
#     first_name= forms.CharField(max_length=50,required=True,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(max_length=50, required=True,
#                                  widget=forms.TextInput(attrs={'class': 'form-control'}))



# class ContactForm(forms.Form):
#     name = forms.CharField(label='Your name', max_length=250)
#     email = forms.EmailField(label='Your email')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 10}))
#     captcha = CaptchaField

class PostCreateForm(forms.ModelForm):
    release_date = forms.DateField(initial=date.today, widget=forms.SelectDateWidget)

    class Meta:
        model = Post

        fields = [
            'title', 'type', 'content', 'image', 'release_date',
        ]

class PostUpdForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'title', 'type', 'content', 'image',
        ]