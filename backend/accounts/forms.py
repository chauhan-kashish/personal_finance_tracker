from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="First name")
    last_name = forms.CharField(max_length=150, required=True, label="Last name")
    email = forms.EmailField(required=True, label="Email", help_text="Required. Enter a valid email address.")
    age = forms.IntegerField(min_value=13, max_value=120, required=True, label="Age")
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True, label="Gender")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "age", "gender", "username", "password1", "password2")
        help_texts = {
            "username": "",
            "password1": "",
            "password2": "",
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
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
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = UserProfile
        fields = ("age", "gender")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.user:
            # Check if email is being changed and if it's already taken by another user
            if email != self.instance.user.email and User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this email already exists.")
        return email
