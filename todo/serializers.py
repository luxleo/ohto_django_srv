from rest_framework import serializers
from .models import Todo

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id','title','complete','created_at','updated_at']

class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title','desc','complete']

class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title','desc']