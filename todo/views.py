from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Todo
from .serializers import TodoListSerializer,TodoCreateSerializer,\
    TodoDetailSerializer

# Create your views here.
class TodoListView(APIView):
    def get(self,req):
        todos = Todo.objects.filter(complete=False)
        serializer = TodoListSerializer(todos,many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    def post(self,req):
        serializer = TodoCreateSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status = status.HTTP_400_BAD_REQUEST)

class TodoDetailView(APIView):
    def get(self,req,pk):
        todo = get_object_or_404(Todo,id=pk)
        serializer = TodoDetailSerializer(todo,many=False)
        return Response(serializer.data, status = status.HTTP_200_OK)
    def put(self,req,pk):
        todo = get_object_or_404(Todo,id=pk)
        serializer = TodoDetailSerializer(todo,data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self,req,pk):
        todo = get_object_or_404(Todo,id=pk)    
        todo.delete()
        #delete의 경우에만 serializer가 필요없다.
        return Response(status=status.HTTP_204_NO_CONTENT)

class DoneTodoListView(APIView):
    def get(self,req):
        todos = Todo.objects.filter(complete=True)
        serializer = TodoListSerializer(todos,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,req):
        serializer = TodoCreateSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save(complete=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)

class DoneTodoDetailView(APIView):
    def get(self,req,pk):
        todo = get_object_or_404(Todo,id=pk)
        serializer = TodoDetailSerializer(todo,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,req,pk):
        todo = get_object_or_404(Todo,id=pk)
        serializer = TodoDetailSerializer(todo,data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,req,pk):
        todo = get_object_or_404(Todo,id=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)