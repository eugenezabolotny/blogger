# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.views.generic.base import View
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from blogger.models import Post
from blogger.forms import PostForm


class MainView(TemplateView):
    template_name = 'posts.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            posts = Post.objects.filter(is_posted=True)
            context = {
                'posts': posts,
                'main_view': True,
            }
            print(posts)
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('main-view')

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginFormView, self).form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('main-view'))


class UsersView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=False).order_by('pk')
        if self.request.user.is_authenticated:
            return queryset


class UserPostsView(TemplateView):
    template_name = 'posts.html'

    def get(self, request, user_id, *args, **kwargs):
        if request.user.is_authenticated:
            author = User.objects.get(pk=user_id)
            all_posts = Post.objects.filter(author_id=user_id)
            posts = all_posts.filter(is_posted=True)
            context = {
                'posts': posts,
                'author': author
            }
            if request.user == author:
                context['posts'] = all_posts
                context['owner'] = True
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})


class PostView(TemplateView):
    template_name = 'post.html'

    def get(self, request, post_id, *args, **kwargs):
        if request.user.is_authenticated:
            author = Post.objects.get(id=post_id).author
            context = {'post_id': post_id}
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                context['post'] = False
            else:
                context['post'] = post
                if request.user == author:
                    context['owner'] = True
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})


class NewPostView(TemplateView):
    template_name = 'edit-post.html'

    def get(self, request, *args, **kwargs):
        form = PostForm()
        if request.user.is_authenticated:
            context = {'form': form}
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = timezone.now()
            post.save()
            return HttpResponseRedirect(reverse('post-view', args=[post.id]))
        else:
            form = PostForm()

        return render(request, self.template_name, {'form': form})


class EditPostView(TemplateView):
    template_name = 'edit-post.html'

    def get(self, request, post_id, *args, **kwargs):
        self.get = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=self.get)
        return render(request, self.template_name, {'form': form})

    def post(self, request, post_id, *args, **kwargs):
        self.post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST, instance=self.post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_at = timezone.now()
            post.save()
            return HttpResponseRedirect(reverse('post-view', args=[post.id]))
        else:
            form = PostForm(instance=self.post)
        return render(request, self.template_name, {'form': form})
