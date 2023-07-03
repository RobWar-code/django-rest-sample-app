from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to = 'images/',
        default = '../default_profile_daov8n'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s Profile"

def create_profile(sender, instance, created, **kwargs):
    if created:
        # Referenced to admin.py
        Profile.objects.create(owner=instance)

# This triggers the create_profile function when the
# record is saved.
post_save.connect(create_profile, sender=User)