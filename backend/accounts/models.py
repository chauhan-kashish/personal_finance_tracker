from django.db import models
from django.contrib.auth.models import User


def user_profile_photo_path(instance, filename):
    """
    Generate file path for new user profile photo uploads.
    Stored under: profile_photos/user_<id>/<filename>
    """
    return f"profile_photos/user_{instance.user.id}/{filename}"


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("P", "Prefer not to say"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(
        upload_to=user_profile_photo_path,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"
