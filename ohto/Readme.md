# Django Local

### Download Source
```
git clone -b django --single-branch git@github.com:luxleo/ohto_django_srv.git
```

### Create and Activate Anaconda Env
```mv to work_dir
cd ohto_django_srv (work)
```
```
conda env create -f env_conf.yaml
```
```
conda activate local_django
```

### Create super user
```
python3 manage.py createsuperuser
```

### Run Django Server On localhost:8000
```
gunicorn --bind 0:8000 ohto.wsgi:application
```

### When run source on production env
```
python3 manage.py runserver --settings=ohto.settings.prod
```
```
#Database config

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
```
### Login with Super user you created before

### If you need update requirements.txt file
```
pip list --format=freeze > requirements.txt
```

### Urls

## admin page (can manipulate, and monitor data) -> localhost:8000/admin
## view API on swagger -> localhost:8000/api/schema/swagger-ui/