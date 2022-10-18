from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

class User(AbstractUser):
    #장고3에서 필드에 선택할 수있는 값 미리 지정한다.
    class GenderChoices(models.TextChoices):
        Male = 'M',"남성"
        Female = 'F',"여성"

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13,validators=[RegexValidator(r"^010-?\d{3}-?\d{4}$")],blank=True)
    gender = models.CharField(max_length=1,choices=GenderChoices.choices, default=GenderChoices.Male,blank=True)
    avatar = models.ImageField(blank=True,upload_to = "accounts/profile/%Y/%m"
    ,help_text="48*48 크기의 png/jpeg파일을 업로드해주세요")
    #django imagekit 라이브러리 이용하여 이미지 처리 할수있다.

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 1

