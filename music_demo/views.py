from rest_framework import status
from rest_framework import permissions,views,viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action

from django.db.models import Q 

from .serializers import PlayListSerializer, SongSerializer
from .models import PlayList, Song, PlayListAndSongJoin
from django.shortcuts import render
import json

# Create your views here.

#커스텀 가능한 permission 객체
class IsOwner(permissions.BasePermission):
    def has_object_permssion(self,request,view,obj):
        return obj.owner == request.user

class LandingView(views.APIView):
    def get(self,req):
        return render(req,'music_demo/layout.html')
index = LandingView.as_view()
class PlayListView(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer

    permission_classes = [IsOwner,permissions.IsAuthenticated]

    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs
    @action(detail=True,methods=['GET'])
    def get_songs(self,req,pk):
        instance = self.get_object()
        song_list = PlayListAndSongJoin.objects.filter(playlist_id=instance.id).values_list('song_id',flat=True)
        res = {"song_list":list(song_list)}

        return Response(data=res,status=status.HTTP_200_OK)
#아래 처럼 개별로 지정 할 수도있고 한꺼번에 router처리도 가능함
#playlist_list_view = PlayListListView.as_view({'get':'list'})


class ModelSongListView(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    filter_backends = [SearchFilter]
    search_fields = ['title','artist']
    def list(self, request,*args,**kwargs):
        search = request.GET.get('search',None)
        queryset = Song.objects.filter(Q(title__icontains=search) | Q(artist__icontains=search))
        serializer = SongSerializer(queryset, many=True)
        return Response({'songs':serializer.data}, template_name='music_demo/song_list.html')

class SongListView(views.APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name = 'music_demo/song_list.html'

    def get(self,req):
        search = req.GET.get('search',None)
        qs = Song.objects.filter(Q(title__icontains=search) | Q(artist__icontains=search))
        return Response({"songs":qs})

song_list = SongListView.as_view()

class InsertSongView(views.APIView):
    def post(self,request):
        playlist_id = request.data.get('playlist_id',None)
        song_id_list = request.data.get('song_id',None)
        for song_id in song_id_list:
            PlayListAndSongJoin.objects.create(playlist_id=playlist_id,song_id=song_id)
        return Response(status=status.HTTP_201_CREATED)



