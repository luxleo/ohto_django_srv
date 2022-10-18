from django.conf import settings
from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    youtube_link = models.URLField(blank=True)
    energy = models.IntegerField(default=-1)
    valence = models.IntegerField(default=-1)

class PlayList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='playlist_owner')
    title = models.CharField(max_length=50)#FIXME set default title regulary
    created_at = models.DateTimeField(auto_now_add=True)

class PlayListAndSongJoin(models.Model):
    playlist_id = models.IntegerField(default=0)
    song_id = models.IntegerField(default=0)

class PlayListTag(models.Model):
    playlist_id = models.IntegerField(default=0)
    tag_name = models.CharField(max_length=50)
    #삭제 같은 경우에 playlist삭제시 이 테이블 다 조회해서 삭제한다
    #또는 플레이리스트 자체 수정일 때는 id 넘겨서 삭제해도 된다.

class SongTag(models.Model):
    song_id = models.IntegerField(default=0)
    tag_name = models.CharField(max_length=50)