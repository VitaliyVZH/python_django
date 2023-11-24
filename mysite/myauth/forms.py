from django import forms

from myauth.models import Profile


class UserCreationForm(forms.ModelForm):
    class Meta:
        permissions = (('change_profile', ),)
