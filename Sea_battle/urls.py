"""
URL configuration for Sea_battle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path

from Sea_battle import settings
from polls.views import index_page, SeaBattle_page, mygift_page, registration, fields, users_page, edit_fields, settings_gift, create_gift,create_board, battle_page

urlpatterns = [
    path('createboard',create_board, name='createboard'),
    path('editfields/<int:board_id>/info', edit_fields, name='editfields'),
    path('battle', battle_page, name='battle'),
    path('creategift/',create_gift),
    path('settingsgift/', settings_gift),
    path('users/', users_page),
    path('fields/', fields, name="fields"),
    path('user/registration/', registration),
    path('admin/', admin.site.urls),
    path('', index_page),
    path('seabattle/', SeaBattle_page),
    path('mygifts/', mygift_page),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
