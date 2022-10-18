from rest_framework.routers import DefaultRouter
from django.urls import include, path

from . import views

router = DefaultRouter()
router.register('playlist',views.PlayListView)

urlpatterns=[
    path('',views.index,name='index'),
    path('song_list/',views.song_list,name='song_list'),
    path('',include(router.urls)),
    path('song_insert',views.InsertSongView.as_view(),name='song_insert')
]