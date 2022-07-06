from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='post_photos', blank=True, null=True)
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

class Comments(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default='User')
    bio = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(upload_to='post_photos', default='post_photos/default_user.jpg')
    location = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()