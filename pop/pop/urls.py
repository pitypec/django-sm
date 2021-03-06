"""pop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from sm.views import (
    home_view,
    tweet_create_view,
    tweet_list_view,
    tweet_detail_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home_view, name='home'),
    path('create-tweet/', tweet_create_view, name='tweet_create_view'),
    path('tweets/', tweet_list_view, name='tweet_list_view'),
    path('tweets/<int:tweet_id>', tweet_detail_view, name='tweet_detail_view'),
    # path('tweets/action', views.tweet_action_view, name='tweet_action_view'),
    # path('tweets/<int:tweet_id>/delete', views.tweet_delete_view, name='tweet_delete_view'),
    path('api/tweets/', include('sm.urls'))
]
