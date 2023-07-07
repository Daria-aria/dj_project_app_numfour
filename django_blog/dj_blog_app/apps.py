from django.apps import AppConfig


class DjBlogAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dj_blog_app'

    def ready(self):
        import dj_blog_app.signals  # noqa