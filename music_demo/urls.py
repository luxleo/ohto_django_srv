from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import http_views,template_views

router = DefaultRouter()
router.register('playlist',http_views.PlayListView)

urlpatterns=[
    path('template/',template_views.landing_page,name='template_index'),
    path('template/song_list/',template_views.song_list,name='template_song_list'),
    path('template/mini_playlists',template_views.mini_playlist,name='mini_playlists'),
    path('template/playlist/<int:pk>/',template_views.PlayListAPI.as_view(),name='playlist'),
    path('template/playlist_list/',template_views.playlist_list,name='template/playlist_list'),
    path('',include(router.urls)),
    path('song_insert',http_views.InsertSongView.as_view(),name='song_insert')
]