from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from gallery.models import Photo   # ✅ this will now work

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "caption"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth', 'gender', 'relation', 'bio', 'picture']







class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "date_of_birth", "gender", "password1", "password2")

def save(self, commit=True):
    user = super().save(commit=False)
    user.first_name = self.cleaned_data.get('first_name')
    user.last_name = self.cleaned_data.get('last_name')
    user.email = self.cleaned_data.get('email')
    if commit:
        user.save()
        profile = user.profile
        profile.phone_number = self.cleaned_data.get('phone_number')
        profile.date_of_birth = self.cleaned_data.get('date_of_birth')
        profile.gender = self.cleaned_data.get('gender')
        profile.bio = self.cleaned_data.get('bio')
        profile.save()
    return user
