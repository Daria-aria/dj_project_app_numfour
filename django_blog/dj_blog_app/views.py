from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from friendship.models import Friend, Follow, Block
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import LoginUserForm, UserForm, UserUpdForm, ProfileUpdForm, PostCreateForm, PostUpdForm
from .models import *

from django.template.loader import render_to_string
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.core.mail import EmailMessage
# from .tokens import account_activation_token

def index(request):
    return render(request, 'homepage.html')


# class RegisterUser(CreateView):
#     form_class = UserForm
#     template_name = 'register.html'
#     # success_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         # user.save()
# def activateEmail(request, user, to_email):
#     mail_subject = 'Activate your user account.'
#     message = render_to_string('activate-account.html', {
#         'user': user.username,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#         'protocol': 'https' if request.is_secure() else 'http'
#     })
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
#                 received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
#     else:
#         messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')
#
# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#
#         messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
#         return redirect('login')
#     else:
#         messages.error(request, 'Activation link is invalid!')
#
#     return redirect('my-posts')


# def register(request):
#     if request.user.is_authenticated:
#         return redirect("/my-posts")
#
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             activateEmail(request, user, form.cleaned_data.get('email'))
#             return redirect('homepage')
#         else:
#             for error in list(form.errors.values()):
#                     messages.error(request, error)
#
#     else:
#         form = UserForm()
#
#     return render(request, 'register.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect("/my-posts")

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


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'my-posts.html'


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'detail.html'


def newpost(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my-posts')
    else:
        form = PostCreateForm()

    return render(
        request=request,
        template_name='new-post.html',
        context={'object': Post, 'form': form}
    )


def updpost(request, post):
    return redirect('/my-posts')


def delpost(request, post):
    if request.method == "POST":
        post.delete()
        return redirect('my-posts')


# @login_required
# def profile(request, username):
#     if request.method == 'POST':
#         user = request.user
#         form = UserUpdForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             user_form = form.save()
#
#             messages.success(request, f'{user_form}, Your profile has been updated!')
#             return redirect('profile', user_form.username)
#
#         for error in list(form.errors.values()):
#             messages.error(request, error)
#
#     user = get_user_model().objects.filter(username=username).first()
#     if user:
#         form = UserUpdForm(instance=user)
#         return render(request, 'profile.html', context={'form': form})
#
#     return redirect("homepage")


def profile(request, username):
    if request.method == 'POST':
        user_form = UserUpdForm(request.POST, instance=request.user)
        profile_form = ProfileUpdForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='my-posts')
    else:
        user_form = UserUpdForm(instance=request.user)
        profile_form = ProfileUpdForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})



def terms(request):
    return render(request, 'terms-policy.html')
