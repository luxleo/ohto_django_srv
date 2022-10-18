from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    #TODO add importance field so that enable sorting accord to it