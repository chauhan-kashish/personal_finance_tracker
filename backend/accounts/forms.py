from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="First name")
    last_name = forms.CharField(max_length=150, required=True, label="Last name")
    age = forms.IntegerField(min_value=13, max_value=120, required=True, label="Age")
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True, label="Gender")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "age", "gender", "username", "password1", "password2")
        help_texts = {
            "username": "",
            "password1": "",
            "password2": "",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                age=self.cleaned_data["age"],
                gender=self.cleaned_data["gender"],
            )
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label="First name")
    last_name = forms.CharField(max_length=150, required=True, label="Last name")

    class Meta:
        model = UserProfile
        fields = ("age", "gender")
