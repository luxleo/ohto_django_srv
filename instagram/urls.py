from django.urls import path,re_path
from . import views
from django.contrib.auth.validators import UnicodeUsernameValidator
app_name = 'instagram'
urlpatterns = [
    path('post/new/', views.post_new,name='post_new'),
    path('post/<int:pk>',views.post_detail,name='post_detail'),
    path('Mypage/<str:user_name>',views.user_page,name='user_page')
]