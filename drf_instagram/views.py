from pipes import Template
from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView,ListAPIView, RetrieveAPIView
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

# class PublicPostListAPIView(ListAPIView):
#     queryset = Post.objects.filter(is_public=True)
#     serializer_class = PostSerializer

#generic 안쓰고 API view 상속 받아서 해보기

class PublicPostListAPIView(APIView):
    def get(self,request):
        qs = Post.objects.filter(is_public=True)
        serializers = PostSerializer(qs,many=True)
        return Response(serializers.data)

#public_post_list_view = PublicPostListAPIView.as_view()

@api_view(['GET'])
def public_post_list_view(req):
    qs = Post.objects.filter(is_public = True)
    serializer = PostSerializer(qs,many=True)
    return Response(serializer.data)

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def dispatch(self,req,*args,**kwargs):
        print("requset body: ",req.body)#print비추천 logger 추천
        print("requset POST: ",req.POST)
        return super().dispatch(req,*args,**kwargs)
    @action(detail=False,methods=['GET'])
    def public(self,req):
        qs = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(qs,many=True)
        return Response(serializer.data)
    @action(detail=True,methods=['PATCH'])
    def set_public(self,req,pk):
        instance = self.get_object()
        instance.is_public = True
        instance.save(update_fields=['is_public'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#rest_framework가 기본적으로 만드는 기능
# def post(req):
#     #2개 분기

# def post_detail(req,pk):
#     #3개 분기

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    renderer_classes=[TemplateHTMLRenderer]
    template_name = 'drf_instagram/post_detail.html'
    def get(self,request,*args,**kwargs):
        post = self.get_object()
        return Response({
            "post":PostSerializer(post).data
        })

