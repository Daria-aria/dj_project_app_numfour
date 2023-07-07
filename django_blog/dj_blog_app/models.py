import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import os



class Post(models.Model):
    class PostType(models.TextChoices):
        Lifestyle = 'L', 'Lifestyle'
        Study = 'S', 'Study'
        Advice = 'A', 'Advice'

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Post', slugify(self.slug), instance)
        return None

    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT, verbose_name='Author')
    title = models.CharField(max_length=150, verbose_name='Title')
    type = models.CharField(max_length=10, choices=PostType.choices, default=None, verbose_name='Type of post')
    content = models.TextField(blank=True, max_length=1000, verbose_name='Content')
    url_width = models.PositiveIntegerField(default=100)
    url_height = models.PositiveIntegerField(default=100)
    image = models.ImageField(upload_to=image_upload_to, width_field='url_width', height_field='url_height', default=None)
    release_date = models.DateField()
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['release_date']


class Profile(models.Model):
    class StatusChoice(models.TextChoices):
        Writer= 'W', 'Writer'
        Follower = 'F', 'Follower'
        Critic = 'C', 'Critic'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userpic = models.ImageField(default='default.jpg', upload_to='media/images/userpic')
    user_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    statusType = models.CharField(max_length=50, choices=StatusChoice.choices, default='n/a')
    bio = models.TextField()
    friends = models.TextField(blank=True)
    followers = models.TextField(blank=True)


#     def __str__(self):
#         return self.user.username

# from django.contrib.auth.models import AbstractUser
# class CustomUser(AbstractUser):
#
#     STATUS = (
#         ('author', 'author'),
#         ('subscriber', 'subscriber'),
#         ('moderator', 'moderator'),
#     )
#
#     username = models.CharField(unique=True, max_length=50)
#     status = models.CharField(max_length=100, choices=STATUS, default=None)
#     description = models.TextField("Description", max_length=600, default='', blank=True)

    # def __str__(self):
    #     return self.username