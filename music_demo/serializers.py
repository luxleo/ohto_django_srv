from rest_framework import serializers
from .models import Song,PlayList

class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = '__all__'
        ordering = ['-created_at']

class PlayListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ['title']

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['title','artist','youtube_link']