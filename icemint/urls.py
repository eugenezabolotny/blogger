"""icemint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blogger import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainView.as_view(), name='main-view'),
    path('login/', views.LoginFormView.as_view(), name='login-view'),
    path('logout/', views.LogoutView.as_view(), name='logout-view'),
    path('users/', views.UsersView.as_view(), name='users-view'),
    path('users/<int:user_id>/', views.UserPostsView.as_view(), name='user-posts-view'),
    path('<int:post_id>/', views.PostView.as_view(), name='post-view'),
    path('create/', views.NewPostView.as_view(), name='new-post-view'),
    path('<int:post_id>/update/', views.EditPostView.as_view(), name='edit-post-view'),
]
