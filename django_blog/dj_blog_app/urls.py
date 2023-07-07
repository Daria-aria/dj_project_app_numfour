from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='homepage'),
    path('my-posts/', PostListView.as_view(), name='my-posts'),
    path('my-posts/<slug:slug>', PostDetailView.as_view(), name='detail'),
    # path('activate/<uidb64>/<token>', activate, name='activate'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logoutuser, name='logout'),
    path('register/', register, name='register'),
    path('profile/<username>', profile, name='profile'),
    path('terms-policy/', terms, name='terms-policy'),

    path("new-post", newpost, name="new-post"),
    path("<post>/upd", updpost, name="upd-post"),
    path("<post>/del", delpost, name="del-post"),
]