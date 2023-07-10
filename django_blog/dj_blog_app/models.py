import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import os
from django.conf import settings
from autoslug import AutoSlugField



class Post(models.Model):
    class PostType(models.TextChoices):
        Lifestyle = 'Lifestyle', 'Lifestyle'
        Study = 'Study', 'Study'
        Advice = 'Advice', 'Advice'

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

    def post_slug(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['release_date']


class Profile(models.Model):
    class StatusChoice(models.TextChoices):
        Writer= 'Writer', 'Writer'
        Follower = 'Follower', 'Follower'
        Critic = 'Critic', 'Critic'

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Profile', slugify(self.username), instance)
        return None

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='user')
    userpic = models.ImageField(upload_to=image_upload_to, default='images/userpic/default.png')
    username = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    statusType = models.CharField(max_length=50, choices=StatusChoice.choices, default='n/a')
    bio = models.TextField()
    friends = models.ManyToManyField("Profile", blank=True)
    followers = models.TextField(blank=True)

    def get_absolute_url(self):
        return "/{}".format(self.slug)


class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Friends1(models.Model):
    users1=models.ManyToManyField(User,null=True)
    current_user=models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE,null=True)

    @classmethod
    def make_friend(cls,current_user,new_friend):
        friend,create=cls.objects.get_or_create(current_user=current_user)
        friend.users1.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(current_user=current_user)
        friend.users1.remove(new_friend)

# class Subscribe(models.Model):
#     from_user = models.ForeignKey('auth.User')
#     to_user = models.ForeignKey('auth.User', related_name="person_subscribers")

# class Friendship(models.Model):
#     to_user = models.ForeignKey('auth.User', related_name="friends")
#     from_user = models.ForeignKey('auth.User')

# class FriendshipRequest(models.Model):
#     to_user = models.ForeignKey('auth.User',
#                                 related_name="friendship_requests_to")
#     from_user = models.ForeignKey('auth.User',
#                                   related_name="friendship_requests_from")
#     status = models.CharField(max_length=25, choices=REQUEST_STATUS,
#                               default=CREATED)