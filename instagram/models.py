from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
import re
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to = 'instagram/post/%Y/%m/%d',blank=True)
    caption = models.CharField(max_length = 500)
    tag_set = models.ManyToManyField('Tag',blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.caption
    
    #model에 detail view있으면 이 함수를 구현하자
    def get_absolute_url(self):
        return reverse("instagram:post_detail", kwargs={"pk": self.pk})
        #or return reverse('model_detail,args=[self.pk])로 해도 가능

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-z\dㄱ-힣]+)",self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag,_ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list
    

class Tag(models.Model):
    #실 서비스에 구현할 때는 django-tagit라이브러리 사용하자.
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name



