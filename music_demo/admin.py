from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Song,PlayList
# Register your models here.

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    #장고 어드민에서 검색 구현할 때는 search_field로 한다.
    #TODO: 서비스 안에서 하려면 view단에 rest_framework.filters.SearchFilter로 구현
    def real_youtube_link(self,song):
        if song.youtube_link != 'dummy':
            return mark_safe(f"<a href='{song.youtube_link}' target='_blank' rel='noopener noreferrer'>{song.youtube_link}</a>")
        return None
    search_fields = ['title','artist']
    list_display=['title','artist','tags','energy','valence','real_youtube_link']

@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display=['owner','created_at','title']
    search_fields = ['owner']

