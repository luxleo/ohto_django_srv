from django.urls import path
from . import views
urlpatterns=[
    path('',views.TodoListView.as_view(),name='todo_list'),
    path('<int:pk>/',views.TodoDetailView.as_view(),name='todo_detail'),
    path('done/',views.DoneTodoListView.as_view(),name='done_todo_list'),
    path('done/<int:pk>',views.DoneTodoDetailView.as_view(),name='done_todo_detail')
]