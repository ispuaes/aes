# -*- coding: utf-8 -*-
from django import forms
from .models import Events, Tasks, Employee, Org, Docs
from django.contrib.admin import widgets


class orgForm(forms.ModelForm):
    class Meta:
        model = Org
        fields = '__all__'


class empForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['lname', 'fname', 'sname', 'phone', 'email', 'post', 'prakt', 'comment']


class evtForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['type', 'date', 'person', 'description']


class tskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['deadline', 'org', 'description']
        widgets = {'deadline': forms.TextInput(attrs={'type': 'date'})}


class loginForm(forms.Form):
    username = forms.CharField(required=True, label=u'Имя пользователя')
    userpass = forms.CharField(required=True, label=u'Пароль', widget=forms.PasswordInput())


class docsForm(forms.ModelForm):
    class Meta:
        model = Docs
        fields = ['number', 'date', 'description', 'file', 'inf']
