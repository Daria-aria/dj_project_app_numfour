from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from friendship.models import Friend, Follow, Block
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import LoginUserForm, UserForm, UserUpdForm, ProfileUpdForm, PostCreateForm, PostUpdForm
from .models import *
import random

from django.template.loader import render_to_string


# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.core.mail import EmailMessage
# from .tokens import account_activation_token

def index(request):
    return render(request, 'homepage.html')


def register(request):
    # if request.user.is_authenticated:
    #     return redirect("/my-posts")

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'New account created: {user.username}')
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        messages.success(self.request, f'You are logged in successfully')
        return reverse_lazy('my-posts')


@login_required
def logoutuser(request):
    logout(request)
    messages.info(request, "You're logged out. Bye")
    return redirect('homepage')


class PostListView(ListView):
    model = Post
    template_name = 'my-posts.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PostListView, self).get_context_data(**kwargs)
    #     # if self.request.user.is_authenticated:
    # # liked = [i for i in Post.objects.all() if Like.objects.filter(user=self.request.user, post=i)]
    # # context['liked_post'] = liked
    # return context


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # liked = [i for i in Post.objects.filter(user_name=user) if Like.objects.filter(user=self.request.user, post=i)]
        # context['liked_post'] = liked
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-release_date')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'detail.html'

@login_required()
def newpost(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            # Post.objects.create(author=request.user, title=form.cleaned_data.get("title"),
            #                     content=form.cleaned_data.get("content"))
            return redirect('my-posts')

    else:
        form = PostCreateForm()

    return render(request, 'new-post.html', {'form': form})



def updpost(request, post):
    return redirect('#')


# def delpost(request, post):
#     if request.method == "POST":
#         post.delete()
#         return redirect('my-posts')
#     return redirect('my-posts')
@login_required
def delpost(request, pk):
	post = Post.objects.get(pk=pk)
	if request.user== post.author:
		Post.objects.get(pk=pk).delete()
	return redirect('my-posts')


@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user)
    if request.method == 'POST':
        user_form = UserUpdForm(request.POST, instance=request.user)
        profile_form = ProfileUpdForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('my-posts')
    else:
        user_form = UserUpdForm(instance=request.user)
        profile_form = ProfileUpdForm(instance=request.user.profile)

    p = request.user.profile  ###
    friends = p.friends.all()  ###
    u = request.user  ### slug deleted from parameters
    sent_friend_requests = Friendship.objects.filter(from_user=request.user)
    rec_friend_requests = Friendship.objects.filter(to_user=request.user)

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(Friendship.objects.filter(
                from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'friend_request_sent'

        # if we have recieved a friend request
        if len(Friendship.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'friends': friends,
        'post_count': user_posts.count,
        'u': u,
        'button_status': button_status,
        # 'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
    }

    return render(request, 'profile.html', context)


@login_required
def profile2(request, username):
    user = get_user_model().objects.filter(username=username).first()
    user_posts = Post.objects.filter(author=user)

    p = Profile.objects.filter(username=username).first()  # instead of slug
    u = user  ###
    sent_friend_requests = Friendship.objects.filter(from_user=user)  ###
    rec_friend_requests = Friendship.objects.filter(to_user=user)  ###
    friends = user.profile.friends.all()  ###

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(Friendship.objects.filter(
                from_user=request.user).filter(to_user=user)) == 1:
            button_status = 'friend_request_sent'

        # if we have recieved a friend request
        if len(Friendship.objects.filter(
                from_user=user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'
    if user:
        user_form = ProfileUpdForm(instance=user.profile)

        context = {
            'user_form': user_form,
            'u': u,
            'button_status': button_status,
            'friends_list': friends,
            'sent_friend_requests': sent_friend_requests,
            'rec_friend_requests': rec_friend_requests,
            'post_count': user_posts.count
        }

        return render(request, 'profile2.html', context)


def terms(request):
    return render(request, 'terms-policy.html')


@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = Friendship.objects.filter(from_user=request.user)
    my_friends = request.user.profile.friends.all()
    sent_to = []
    friends = []
    for user in my_friends:
        friend = user.friends.all()
        for f in friend:
            if f in friends:
                friend = friend.exclude(user=f.user)
        friends += friend
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 4))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends += random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    for se in sent_friend_requests:
        sent_to.append(se.to_user)
    context = {'users': friends, 'sent': sent_to}
    return render(request, "users_list.html", context)


def friend_list(request):
    p = request.user.profile
    friends = p.friends.all()
    context = {'friends': friends}
    return render(request, "friend_list.html", context)


@login_required
def send_friend_request(request, id):
    # user = get_user_model().objects.filter(id=id).first()
    user = get_object_or_404(User, id=id)
    frequest, created = Friendship.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    print('friend request sent')
    return HttpResponseRedirect('/profile/{}'.format(user.profile.slug))


@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = Friendship.objects.filter(
        from_user=request.user,
        to_user=user).first()
    frequest.delete()
    return HttpResponseRedirect('/profile/{}'.format(user.profile.slug))


@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = Friendship.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if (Friendship.objects.filter(from_user=request.user, to_user=from_user).first()):
        request_rev = Friendship.objects.filter(from_user=request.user, to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    print('Request accepted')
    return HttpResponseRedirect('/profile/')


@login_required
def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = Friendship.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    print('Request rejected')
    return HttpResponseRedirect('/profile/{}'.format(from_user.profile.slug))


def delete_friend(request, id):
    user_profile = request.user.profile
    friend_profile = get_object_or_404(Profile, id=id)
    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)
    print('Friend deleted')
    return HttpResponseRedirect('/profile/{}'.format(friend_profile.slug))
