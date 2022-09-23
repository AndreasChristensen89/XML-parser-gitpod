from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Profile


class UserForm(UserChangeForm):
    """View and edit user"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        """Meta class"""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            )


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['experimentalist_uid']

class ProfileForm(forms.Form):
    """
    Form to update profil's information
    """
    experimentalist_uid = forms.CharField(required=False)
