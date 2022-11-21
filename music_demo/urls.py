from rest_framework.routers import DefaultRouter
from django.urls import include, path
from django.conf import settings

from .views import http_views,template_views


router = DefaultRouter()
router.register('playlist',http_views.PlayListView)


urlpatterns=[
    path('',include(router.urls)),
    path('songs/',http_views.SongListView.as_view()),
    path('songs/<int:pk>/',http_views.SongDetailView.as_view()),
    path('songs/search/',http_views.SongSearchView.as_view()),
    path('songs/recommand_this_song/<int:pk>/',http_views.SongRecommendView.as_view()),
    path('songs/filter_by_tags/',http_views.SongFilterByTagView.as_view()),
    path('tags/',http_views.TagListView.as_view())
]

template_urlpatterns=[
    path('template/',template_views.landing_page,name='template_index'),
    path('template/song_list/',template_views.song_list,name='template_song_list'),
    path('template/filter_song/<str:tag_group>/<str:tag_name>/',template_views.FilterSongByTagView.as_view(),name='filter_song_by_tag'),
    path('template/mini_playlists',template_views.mini_playlist,name='mini_playlists'),
    path('template/playlist/<int:pk>/',template_views.PlayListAPI.as_view(),name='playlist'),
    path('template/playlist_list/',template_views.playlist_list,name='template/playlist_list'),
    path('template/Mypage/<str:user_name>',template_views.UserPageView.as_view(),name='template_user_page'),
]
if not settings.DEBUG:
    urlpatterns+=template_urlpatterns