from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'type', 'release_date', 'content', 'image')
    list_display_links = ('author', 'title')
    readonly_fields = ()
    search_fields = ('title', 'content')
    list_editable = ('image', 'type')
    list_filter = ('type',)
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-empty-'

    def get_image(self, object):
        if object.image:
            return mark_safe(f'<img scr="{object.image.url}" width=100>')

    get_image.short_description = 'Image object'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'username', 'userpic', 'date_of_birth', 'statusType', 'bio')
    list_display_links = ('user', 'username')
    search_fields = ('user', 'statusType')


    def get_image(self, object):
        if object.userpic:
            return mark_safe(f'<img scr="{object.userpic.url}" width=100>')

    get_image.short_description = 'Userpic object'

admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Friendship)
admin.site.register(Friends1)


