from .common import *
#안티 패턴이지만 settings 에서는 모든 파일을 임포트 해와야 하므로 허용한다.
#TODO: 3000곡 필드 다 채워넣기
#TODO: staticfile 경로 s3를 하든 file system을 이용하든
#TODO: 이미지 경량화
#TODO: 크롤링할 데이터: 각 곡당 커버이미지, 유튜브 url,가사(인수님 한테 물어보자)
#TODO: 전문조회 한다면 일라스틱 서치와 postgres 전문 조회 비교
#TODO: postgres사용시 cache하여 db부하 줄이기


#TODO:Let's encrypt로 ssl인증 발급

#docker run 시
#NOTE: 데이터 옮길때 mysql 설정: docker run -d -p 3306:3306 --name django-mysql -v `pwd`/data:/var/lib/mysql mysql

#NOTE: linux os 환경변수 설정: /etc -> cat << EOD >> bash.bashrc -> export PROD=--settings=...

#NOTE: 1. docker run -it --name django-main -p 8000:8000 --link django-mysql django-main
#NOTE: 2. docker start -i django-main

#vim 설치방법
#NOTE: 1.apt-get update -> 2.apt-get install vim

#db 구성시
#NOTE: CREATE DATABASE <dbname> CHARACTER SET utf8;

#prod setting migration할 때 
#NOTE: python3 manage.py makemigrations $PROD -> python3 manage.py migrate $PROD

#TODO:이미지 환경변수 env ['PROD','P3M']에 추가하기 

#TODO:docker image hub에  django project 이미지 배포하기
#TODO: elk 스택 대신 redis로 song(3000) 캐쉬해놓고 사용
#TODO: postgres 디비에서 지원하는 기본 기능 이용
#TODO: compare each speed between using foreign key and query set using id_list
#NOTE: prod 환경 설정시 debug false하여 메모리에 쿼리 누적되는것 방지 -> allowed-hosts에 지정된 호스트들만 접근 가능하게 설정


DEBUG = os.environ.get('DEBUG') in ['true','True']

INSTALLED_APPS = [
    #django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Third Apps
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'drf_spectacular',
    #Local App
    'accounts',
    'music_demo'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':'django_db',
        'USER':'root',
        'PASSWORD':'1234',
        'HOST':'django-mysql',
        'PORT':'3306'
    }
}

#TODO: 1.error 로그 관리 sentry서비스 이용하여 체계적으로 관리 될 수 있도록 하자.
LOGGING = {
    "version":1,
    "disable_existing_loggers":False,
    "handlers":{"console":{"level":"ERROR", "class":"logging.StreamHandler"}},
    "loggers":{"django":{"handlers":["console"],"level":"ERROR"}}
}