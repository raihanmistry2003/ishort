from allauth.account.forms import SignupForm
from django import forms
from functions.models import (
    Url
)

class AllauthSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, required=True, label='First Name')
    last_name = forms.CharField(max_length=50, required=True, label='Last Name')

    def save(self, request):
        user = super(AllauthSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

# class UrlForm(forms.ModelForm):
#     class Meta:
#         model = Url
#         fields = ('long_url', 'url_title')