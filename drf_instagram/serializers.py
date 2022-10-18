from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

#클래스 상속해줘서 serializer 필드 구현
class AuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()#User이렇게 가져오지 않는다.
        fields = ['email','username']


class PostSerializer(ModelSerializer):
    user_name = serializers.ReadOnlyField(source='writer.username')
    #writer = AuthorSerializer()
    class Meta:
        model = Post
        fields = [
            'created_at','user_name','message','is_public'
        ]