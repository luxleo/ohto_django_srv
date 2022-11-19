from rest_framework import status
from rest_framework import permissions,views,viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

#TODO: 태그 검색구현하기
#TODO: api명세 
#NOTE: action 데코레이터로 viewset에서 커스텀 api구축 가능하다. ex)@action(detail=True,methods=["GET"])
from rest_framework.decorators import action

from django.db.models import Q 

import json

from ..serializers import PlayListSerializer, SongSerializer,PlayListSongJoinSerializer
from ..models import PlayList, Song, PlayListAndSongJoin

#NOTE: DRF에서는 as_view함수 호출시 django csrf_exepmt가 데코레이터로 감싸져 csrf체크를 하지 않는다.
#NOTE: api_view데코레어터로 작업하면 get,post.del,put 원하는 메소드만 명세하여 작업하므로 좀 가벼워진다.
#NOTE: APIView -> mixin -> generic -> viewset 으로 정리가 되어있고 mro(method resolution order)를 지키며 구성되어있다.
# Create your views here.

#커스텀 가능한 permission 객체
class IsOwner(permissions.BasePermission):
    def has_object_permssion(self,request,view,obj):
        return obj.owner == request.user

class MyPaginationClass(PageNumberPagination):
    page_size=10
    page_size_query_param='page_size'
    max_page_size=10

class SongSearchView(views.APIView):
    permission_classes=[permissions.IsAuthenticated]
    @extend_schema(
        request=SongSerializer,
        responses={200:SongSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),
            OpenApiParameter(name='search',description="query string 형식으로 보내며 키는 search로 보낸다."),
        ],
        summary='jwt 필요, search키 값에 들어온 제목이나 아티스트를 포함하는 곡들을 반환한다.',
        examples=[
            OpenApiExample(
            'search 쿼리스트링으로 검색할때.',
            description="쿼리스트링에 search 키값으로 제목이나 가수를 넘긴다.",
            value='/songs/search/?search=<str:검색값>'
        ),
        OpenApiExample(
            'search 검색 반환값.',
            description="곡중 제목이나 가수를 포함하는 곡들을 반환한다.",
            value=[
                {"id":1,"title":"곡 제목(str)","artist":"가수(str)","tags":"str","youtube_link":"link(str)"},
                {"id":2,"title":"곡 제목(str)","artist":"가수(str)","tags":"str","youtube_link":"link(str)"},
                {"id":3,"title":"곡 제목(str)","artist":"가수(str)","tags":"str","youtube_link":"link(str)"}
                ]
        )]
    )
    def get(self,req,format=None):
        search=req.GET.get('search',None)
        qs = Song.objects.filter(Q(title__icontains=search) | Q(artist__icontains=search)).order_by('id')[:10]
        serializer = SongSerializer(qs,many=True)
        return Response({"songs":serializer.data,"length":len(serializer.data)})

class SongRecommendView(views.APIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class= SongSerializer
    pagination_class = MyPaginationClass

    @property
    def paginator(self):
        if not hasattr(self,'_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self,queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,self.request,view=self)

    def get_paginated_response(self,data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


    @extend_schema(
        request=SongSerializer,responses={200:SongSerializer},
        parameters=[
            OpenApiParameter.HEADER,OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),OpenApiParameter(name='pk',description="추천 받고자하는 곡의 id이다"),
        ],
        summary='jwt 필요, 추천 받고자 하는 곡의 가사기반 태그와 e,vlabel 이 같은 곡들을 paginating형식으로 반환 (한 페이지에 10곡씩 최대 100곡까지 추천).',
        examples=[
            OpenApiExample(
            "id 8900곡 추천 곡 요청할때",
            description="쿼리스트링에 search 키값으로 제목이나 가수를 넘긴다.",
            value='http://localhost:8000/songs/recommand_this_song/8900/?page=2'
        ),
        OpenApiExample(
            'id 8900곡 추천 곡 요청 반환값.',
            description="곡중 제목이나 가수를 포함하는 곡들을 반환하고 이전 페이지 이후 페이지 반환한다.",
            value={
            'links': {
                'next': "http://localhost:8000/songs/recommand_this_song/8900/?page=3",
                'previous': "http://localhost:8000/songs/recommand_this_song/8900/"
            },
            'count': 100,
            'results': [
        {
            "id": 8844,
            "title": "주저하는 연인들을 위해",
            "artist": "잔나비",
            "youtube_link": "https://youtube.com/watch?v=5g4KsIizYhQ",
            "tags": "[\"연인\", \"슬픔\", \"휴식\"]"
        },
        {
            "id": 8845,
            "title": "Someone Like You",
            "artist": "Adele",
            "youtube_link": "https://youtube.com/watch?v=hLQl3WQQoQ0",
            "tags": "[\"연인\", \"잔잔한\", \"휴식\"]"
        },
        {
            "id": 8846,
            "title": "너의 모든 순간",
            "artist": "성시경",
            "youtube_link": "https://youtube.com/watch?v=evOsUf9en-Y",
            "tags": "[\"연인\", \"그리움\", \"휴식\"]"
        },
        {
            "id": 8847,
            "title": "비도 오고 그래서 (Feat. 신용재)",
            "artist": "헤이즈 (Heize)",
            "youtube_link": "https://youtube.com/watch?v=afxLaQiLu-o",
            "tags": "[\"연인\", \"슬픔\", \"휴식\"]"
        },
        {
            "id": 8848,
            "title": "걱정말아요 그대",
            "artist": "이적",
            "youtube_link": "https://youtube.com/watch?v=Dic27EnDDls",
            "tags": "[\"위로\", \"잔잔한\", \"휴식\"]"
        },
        {
            "id": 8849,
            "title": "우주를 줄게",
            "artist": "볼빨간사춘기",
            "youtube_link": "https://youtube.com/watch?v=9U8uA702xrE",
            "tags": "[\"연인\", \"기쁨\", \"운동\"]"
        },
        {
            "id": 8850,
            "title": "Beautiful",
            "artist": "Crush",
            "youtube_link": "https://youtube.com/watch?v=_5TJcaHO2gU",
            "tags": "[\"연인\", \"그리움\", \"휴식\"]"
        },
        {
            "id": 8852,
            "title": "선물",
            "artist": "멜로망스(Melomance)",
            "youtube_link": "https://youtube.com/watch?v=qYYJqWsBb1U",
            "tags": "[\"연인\", \"잔잔한\", \"휴식\"]"
        },
        {
            "id": 8853,
            "title": "좋니",
            "artist": "윤종신",
            "youtube_link": "https://youtube.com/watch?v=jy_UiIQn_d0",
            "tags": "[\"이별\", \"그리움\", \"휴식\"]"
        },
        {
            "id": 8855,
            "title": "Lost Stars",
            "artist": "Adam Levine",
            "youtube_link": "https://youtube.com/watch?v=cL4uhaQ58Rk",
            "tags": "[\"연인\", \"신나는\", \"운동\"]"
        }
    ]
        }
        )]
    )
    def get(self,req,pk,format=None,*args,**kwargs):
        current_song= get_object_or_404(Song,id=pk)

        energy=current_song.energy
        valence = current_song.valence
        if current_song.tags != '':
            tags = json.loads(current_song.tags)
            topic_tag = tags[0]
            situation_tag = tags[-1]
            instance = Song.objects.filter(Q(energy=energy)&Q(valence=valence)&(Q(tags__icontains=topic_tag) | Q(tags__icontains=situation_tag)))[:100]
            page = self.paginate_queryset(instance)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page,many=True).data)
            else:
                serializer = self.serializer_class(instance,many=True)
            return Response(serializer.data)
        instance = Song.objects.filter(energy=energy,valence=valence)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(instance,many=True).data)
        else:
            serializer= self.serializer_class(instance,many=True)
        return Response({"recommended_songs":serializer.data,"length":len(instance)})

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
    def perform_destroy(self, instance):
        #delete시 playlist안에 있는 노래까지 삭제
        instance_id = instance.id
        PlayListAndSongJoin.objects.filter(playlist_id=instance_id).delete()
        return super().perform_destroy(instance)
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),
        ],
        summary='jwt 필요, 해당 id의 플레이리스트에 들어있는 곡들을 반환한다.',
        examples=[
            OpenApiExample(
            "GET api 날리고 받는 json필드",
            description="song_list 키 안에 현재 플레이리스트에 들어있는 곡들의 id 리스트 받는다..",
            value={"song_list":[1,2,3,4,5,14,24]}
        )]
    )
    @action(detail=True,methods=['GET'])
    def get_songs(self,req,pk):
        #playlist/<int:playlist_id>/get_songs/로 접근하여 해당 playlist안에 곡들 반환
        instance = self.get_object()
        song_list = PlayListAndSongJoin.objects.filter(playlist_id=instance.id).values_list('song_id',flat=True)
        songs = Song.objects.in_bulk(song_list)
        serializer = self.get_serializer()
        res = {"song_list":list(song_list)}
        print(type(song_list))
        return Response(data=res,status=status.HTTP_200_OK)
    @extend_schema(
        request=PlayListSerializer,
        responses={201:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),
            OpenApiParameter(name='songs',description="플레이리스트 내에서 추가할 곡들의 id 리스트이다."),
        ],
        summary='jwt 필요, 해당 id의 플레이리스트에 들어있는 곡 중 추기하고 싶은 곡의 아이디를 넣자 -> 추가가 되었다.',
        examples=[
            OpenApiExample(
            "POST api 날릴때 json필드",
            description="songs 키 안에 현재 플레이리스트에 들어있는 추가할 곡 id 리스트 날리자.",
            value={"songs":[1,2,3,4,5,14,24]}
        ),OpenApiExample(
            "POST api 날리고 받는 json필드",
            description="songs 키 안에 현재 플레이리스트에 들어있는 추가할 곡 id 리스트 날리자.",
            value="아무것도 반환 하지 않는다 상태코드 201만 반환"
        )]
    )
    @action(detail=True,methods=["POST","PUT"])
    def insert_songs(self,req,pk):
        #playlist/<int:playlist_id>/insert_songs/로 접근하여 해당 playlist안에 곡 추가
        instance_id = self.get_object().id
        print(req.data)
        song_list = req.data.get("songs",None)
        #TODO: song_list비어있으면 redirect하기
        for id in song_list:
            join_serializer=PlayListSongJoinSerializer(data={"song_id":id,"playlist_id":instance_id})
            if join_serializer.is_valid():
                join_serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 실을 웹토큰 필수로 넣어야한다."),
            OpenApiParameter(name='songs',description="플레이리스트 내에서 삭제할 곡들의 id 리스트이다."),
        ],
        summary='jwt 필요, 해당 id의 플레이리스트에 들어있는 곡 중 삭제하고 싶은 곡의 아이디를 넣자 -> 삭제가 되었다.',
        examples=[
            OpenApiExample(
            "delete api 날릴때 json필드",
            description="songs 키 안에 현재 플레이리스트에 들어있는 삭제할 곡 id 리스트 날리자.",
            value={"songs":[1,2,3,4,5,14,24]}
        )]
    )
    @action(detail=True,methods=["POST"])
    def delete_songs(self,req,pk):
        #playlist/<int:playlist_id>/delete_songs/로 접근하여 해당 playlist안에 선택한 곡 삭제
        instance_id = self.get_object().id
        song_list = req.data.get("songs",None)
        for song_id in song_list:
            qs = PlayListAndSongJoin.objects.get(song_id=song_id,playlist_id=instance_id)
            qs.delete()
        return Response(status=status.HTTP_200_OK)
    #NOTE:기본 메서드 list,create,retrieve,update,partial_update,destroy 6가지 있음
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="헤더에 토큰 담아서 get 요청하면 된다."),
        ],
        summary='jwt 필요, 유저가 현재 가지고 있는 플레이리스트 반환.',
        examples=[
            OpenApiExample(
            "list조회시",
            description="유저가 가지고 있는 플레이리스트 반환.",
            value=[
                {"id": 0,"title": "string","desc": "플레이리스트 설명string","cover_img": "img_url(str)"},
                {"id": 1,"title": "string","desc": "string","cover_img": "img_url(str)"},
                {"id": 2,"title": "string","desc": "string","cover_img": "img_url(str)"},]
        )]
    )
    def list(self,req,format=None):
        return super().list(req)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="입력한대로 플레이리스트 만들고 id필드 추가해서 같이 반환."),
        ],
        summary='jwt 필요, 입력한 대로 플레이리스트 생성.',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 반환."),
        ],
        summary='jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 반환.',
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 수정."),
        ],
        summary='jwt 필요, 조회한 id와 일치하는 플레이리스트 수정. title은 필수필드 이므로 비워서는 안된다.',
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 수정."),
        ],
        summary='jwt 필요, 조회한 id와 일치하는 플레이리스트 수정. title은 필수필드 이므로 비워서는 안된다.',
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @extend_schema(
        request=PlayListSerializer,
        responses={200:PlayListSerializer},
        parameters=[
            OpenApiParameter.HEADER,
            OpenApiParameter(name='jwt.token',description="jwt 필요, 유저가 보유한 플레이리스트 중, 조회한 id와 일치하는 플레이리스트 삭제."),
        ],
        summary='jwt 필요, 조회한 id와 일치하는 플레이리스트 삭제.',
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

#아래 처럼 개별로 지정 할 수도있고 한꺼번에 router처리도 가능함
#playlist_list_view = PlayListListView.as_view({'get':'list'})





