"""
URL configuration for eventHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from sys import path_hooks
from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path

from userportal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registration/', views.registration, name='registration'),
    path('events/', views.events, name='all_events'),  # URL for viewing all events
    path('events/<int:event_id>/', views.view_event, name='view_event'),
    path('events/<int:event_id>/', views.view_event, name='event_detail'),
    path('edit_event/<int:id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:id>/', views.delete_event, name='delete_event'),
    path('register/', views.register_view, name='register'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    path('remove_from_cart/<int:ticket_id>/', views.remove_from_cart, name='remove_from_cart'),

]
