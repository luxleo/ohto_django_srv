# Django Local

### Download Source
```
git clone -b django --single-branch git@github.com:luxleo/ohto_django_srv.git
```

### Create and Activate Anaconda Env
```
cd ohto_django_srv (work)
```
```
conda env create -f env_conf.yaml
conda activate local_django
```

### Create super user
```
python3 manage.py createsuperuser
```

### Run Django Server On localhost:8000
```
python3 manage.py runserver
```

### Urls
## admin page (can manipulate, and monitor data) -> localhost:8000/admin
## view API on swagger -> localhost:8000/api/schema/swagger-ui/