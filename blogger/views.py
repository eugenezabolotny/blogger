# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from blogger.models import Post
from django.urls import reverse, reverse_lazy



class MainView(TemplateView):
    template_name = 'body.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            posts = Post.objects.all()
            context = {'posts': posts}
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
            posts = Post.objects.filter(author_id=user_id, is_posted=True)
            print(posts[0])
            author = User.objects.get(pk=user_id)
            context = {
                'posts': posts,
                'author': author
            }
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})


class PostView(TemplateView):
    template_name = 'post.html'

    def get(self, request, post_id, *args, **kwargs):
        if request.user.is_authenticated:
            context = {'post_id': post_id}
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                context['post'] = False
            else:
                context['post'] = post
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})
