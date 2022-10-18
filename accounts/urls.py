from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('signup/', views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('password_change',views.change_password,name='change_password'),
    path('profile_edit',views.profile_edit,name='profile_edit')
]