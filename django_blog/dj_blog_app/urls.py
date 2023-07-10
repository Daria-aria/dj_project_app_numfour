from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='homepage'),
    path('my-posts/', PostListView.as_view(), name='my-posts'),
    path('my-posts/<slug:slug>', PostDetailView.as_view(), name='detail'),
    # path('activate/<uidb64>/<token>', activate, name='activate'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logoutuser, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/<username>', profile2, name='profile2'),
    path('terms-policy/', terms, name='terms-policy'),
    path("new-post/", newpost, name="new-post"),
    path("<post>/upd", updpost, name="upd-post"),
    path("del-post/<int:pk>", delpost, name="del-post"),

    path('users_list/', users_list, name='users_list'),
    path('user_posts/<str:username>', UserPostListView.as_view(), name='user_posts'),
    path('friend_list/', friend_list, name='friend_list'),
    path('friend-request/send/<int:id>', send_friend_request, name='send_friend_request'),
    path('friend-request/cancel/<int:id>/', cancel_friend_request, name='cancel_friend_request'),
    path('friend-request/accept/<int:id>/', accept_friend_request, name='accept_friend_request'),
    path('friend-request/delete/<int:id>/', delete_friend_request, name='delete_friend_request'),
    path('friend/delete/<int:id>/', delete_friend, name='delete_friend'),

]
