"""
URL configuration for webapps project.

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
from django.urls import path, re_path
import data_management.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start_page, name='home'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('main', views.start_page, name="main"),
    path('input', views.input_page, name="input"),
    path('search', views.search_page, name="search"),
    path('chip', views.chip_page, name="chip"),
    re_path(r'csv_output/<int:csv_id>/$', views.csv_output, name='csv_output'),
    re_path(r'csv_output_selected/<int:csv_id>/$', views.csv_output_selected, name='csv_output_selected'),
    path('photo/<slug:process>/<int:chip_id>', views.get_photo, name='photo'),
    path('central', views.central_action, name='central'),
    path('chipnum/<int:chip_id>', views.display_chip, name='chipnum'),
    path('mypfp', views.mypfp_action, name='mypfp'),
    path('otherpfp/<int:user_id>/', views.otherpfp_action, name='otherpfp'),
]
