from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from requests import request
from .models import Post, Comments, UserProfile, User
from django.views import View
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
class PostistView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(author__profile__followers__in=[logged_in_user.id]).order_by('-created_on')
        user_profile = UserProfile.objects.get(user=request.user)
        form = PostForm()
        for post in posts:
            like = post.likes.all()
            for liked_by in like:
                if liked_by == request.user:
                    already_liked = True
                    break
                else:
                    already_liked = False
        context = {
            'post_list': posts,
            'form'     : form,
            'user_profile': user_profile,
            'already_liked': already_liked
        }
        return render (request, 'social/post_list.html', context)
    
    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.all()
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit= False)
            new_post.author = request.user
            new_post.save()
            context = {
            'post_list': posts,
            'form'     : form
            }
            return redirect ('posts:post-list')

class PostDetailView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
            post = Post.objects.get(pk=pk)
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.post = post
                new_comment.save()
            
            comments = Comments.objects.filter(post=post).order_by('-created_on')
            context = {
                'post': post,
                'form': form,
                'comment_list': comments,
            }
            return render(request, 'social/post_detail.html', context)

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        comment = Comments.objects.filter(post=post).order_by('created_on')
        form = CommentForm()
        context = {
            'post': post,
            'comment_list': comment,
            'form': form,
        }
        return render (request, 'social/post_detail.html', context)

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('posts:post-list')

def delete_comment(request, id):
    comment = Comments.objects.get(id=id)
    comment.delete()
    return redirect('posts:post-list')

@login_required()
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = UserProfile.objects.get(user=user_object)
    posts = Post.objects.filter(author=user_object).order_by('-created_on')
    followers = user_profile.followers.all()
    for follower in followers:
        if follower == request.user:
            is_following = True
            break
        else:
            is_following = False
    number_of_followers = len(followers)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return HttpResponseRedirect(request.path_info)

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
            'object': user_object,
            'profile': user_profile,
            'posts':posts,
            'number_of_followers': number_of_followers,
            'p_form':p_form,
            'is_following':is_following
    }
    return render(request, 'social/profile.html', context)

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user_object = User.objects.get(username=pk)
        user_profile = UserProfile.objects.get(user=user_object)

        user_profile.followers.add(request.user)
        return redirect ('profile', pk=user_object.username)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user_object = User.objects.get(username=pk)
        user_profile = UserProfile.objects.get(user=user_object)

        user_profile.followers.remove(request.user)
        return redirect ('profile', pk=user_object.username)

class Addlike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        post.likes.add(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class Removelike(LoginRequiredMixin, View):
    def post(self, request, pk, *args,**kwargs):
        post = Post.objects.get(pk=pk)

        post.likes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class FollowerList(View):
    def get(self, request, pk, *args, **kwargs):
        user_object= User.objects.get(username=pk)
        user_profile= UserProfile.objects.get(user=user_object)
        followers = user_profile.followers.all()
        
        context = {
            'profile': user_profile,
            'followers': followers
        }
        return render(request, 'social/followers_list.html', context)

def search_view(request):
    if request.method=="POST":
        searched = request.POST.get('searched')
        queryset = UserProfile.objects.filter(user__username__contains=searched)
        context = {'searched':searched,
                 'items':queryset}
        return render(request, 'social/search.html', context)
    else:
        return render(request, 'social/search.html')

def handle_not_found(request, exception):
    return render(request, 'not-found.html')