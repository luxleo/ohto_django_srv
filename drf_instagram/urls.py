from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
app_name='drf_instagram'
router = DefaultRouter()
router.register('post',views.PostViewSet)#2개의 url을 만든다
#router.urls url리스트를 반환한다.
urlpatterns=[
    path('',include(router.urls)),
    path('post_detail/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('public/',views.public_post_list_view,name='public_post_list')
]
