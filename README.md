# Cobra

![](https://img.shields.io/badge/Python-3.10.9-blue)
![](https://img.shields.io/badge/Django-4.1.5-%2344B78B)
![](https://img.shields.io/badge/REST%20Framework-3.14.0-%23A30000)
![](https://img.shields.io/badge/Swagger-OpenAPI%202.0-%23aaaa00)
![](https://img.shields.io/badge/LICENSE-MIT-%2300557f)

A custom server program based on the **Django framework** designed 
to allow a programmer to directly move to the implementation of 
an application's features without having to torture himself with other time-consuming 
configuration or installation. <br/>

This is the list of the installed features :
1. **Django REST Framework** : it's a powerful and flexible toolkit for building Web APIs.
2. **drf-yasg** : for the generation of a documentation of the API in real `Swagger/OpenAPI 2.0 specifications` from a `Django Rest Framework` API.
3. **Django CORS Headers** : it's a security mechanism that `allows one domain to access` resources hosted on `another domain`.


## Installation
We must install three (03) programs:
1. `Python3` runtime;
2. Python virtual environment `venv`;
3. Database manager `PostgreSQL`;
4. Getting of project repository.

### Install `python3`

```sh
sudo apt install python3 python3-pip
```

You have to make sure of the version of python that is installed.
The version of python used is `python 3.10.9`.

### Install venv
You can install a python virtualenv program in two different ways.

```sh
sudo apt install python3-venv
```

OR

```sh
sudo pip3 install virtualenv
```

### Install `PostgreSQL`

```sh
sudo apt install postgresql postgresql-contrib
```

For using a `spacial database`, we can install the following extension:

```sh
# PostGIS is an extension of PostgreSQL
# that allows to process the spacial data like the Polygons,
# the Points, ...
sudo apt install postgis
```

### Getting of project repository
You can clone this repository everywhere you want in your machine,
with the following command lines:

```sh
git clone https://github.com/mokira3d48/cobra.git myapp && cd myapp
```

In this cloned directory, you will see the following structure:

```
.
├── LICENSE
├── README.md
├── requirements.txt
└── server
    ├── core
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── manage.py

2 directories, 9 files
```

## Configuration
1. Setting virtual environment;
2. Creating and setting of PostgreSQL database;
3. Dependences installation.

### Setting virtual environment
1. In your project root, if you have not already done so,
run one of the following commands to create a virtual environment.

```sh
python3 -m venv env
```

OR

```sh
virtualenv env -p python3
```

2. Launch environment

```sh
source env/bin/activate
```

3. You must execute the following command to install the basic dependences:

```sh
pip install -r requirements.txt
```

### Creating and setting of PostgreSQL database
The following `SQL` command lines allow to create a `PostgreSQL`
database for your application:

```sh
# To connect to PostgreSQL with ROOT user:
sudo su - postgres

```

```sh
# To connect to default database (postgres)
psql

```

Given your database name is `cbrdb` and the username is `cobra`.

```sql
CREATE DATABASE cbrdb;
CREATE USER cobra WITH ENCRYPTED PASSWORD 'your-secret-password-here';
ALTER ROLE cobra SET client_encoding TO 'utf8';
ALTER ROLE cobra SET default_transaction_isolation TO 'read committed';
ALTER ROLE cobra SET timezone TO 'Europe/Paris';
GRANT ALL PRIVILEGES ON DATABASE cbrdb TO cobra;

-- configuration for testing database for Django
ALTER USER cobra CREATEDB;
ALTER ROLE cobra SUPERUSER;

-- connect to brydb
\c cbrdb
```

```sql
-- ...

-- Only you are using a spatial database
CREATE EXTENSION postgis;
```

Finally, disconnect from PostgreSQL by pressing `CTRL + D` twice.


#### .env config

1. You have to create a `.env` file in the root of the server
from the `server/.env_example`:

```sh
cp server/.env_example server/.env
```

2. Insert the following information into `.env` file:

| FIELDS   | VALUES                    |
| ------   | --------------------------|
| DB_NAME  | cbrdb                     |
| USERNAME | cobra                     |
| PASSWORD | your-secret-password-here |
| HOST     | 127.0.0.1                 |
| PORT     | 5432                      |

Here are the contents of the file `.env`:

```
DB_NAME=cbrdb
USERNAME=cobra
PASSWORD=your-secret-password-here
HOST=127.0.0.1
PORT=5432

```

> If port `5432` does not work, then try port `5433`.

## Launching the server
- Execute the following command lines to make migrations of models into database. 
It's assumed that you are currently in project directory root `cobra`.

```sh
mkdir server/static;\
./server/manage.py makemigrations;\
./server/manage.py migrate
```

You will get the following result, if all works succefully :

```
No changes detected
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  
  ...
  
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK

```

- Then, create a super user that will be used to connect to admin space.

```sh
./server/manage.py createsuperuser
```

- Finally to start server, you must execute the following command line:

```sh
./server/manage.py runserver
```

The result is :

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 21, 2022 - 22:07:54
Django version 3.2.6, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```

We cant go it at this local host link [](http://127.0.0.1:8000/) or [](http://localhost:8000). <br/>
You can change the IP address and the port of the server with the following command line:

```sh
# With this command, we cant make the server listens
# on the IP address of your local network on the port 8080.
./server/manage.py runserver 0.0.0.0:8080
```

You will see :

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 21, 2022 - 22:08:41
Django version 3.2.6, using settings 'core.settings'
Starting development server at http://0.0.0.0:8080/
Quit the server with CONTROL-C.

```

All work with successfully ! <br/>
To access it in this cas, you must execute the following command line, in first:

```sh
# IF YOU ARE USING LINUX
# show your IP address of your machine, if it's connected
# to your local network for example.
ifconfig
```

> For the people using **Windows**, use `ipconfig` insted of the command line above.

We cant go it at this local host [link](http://yourip:8080/).

## Usage

1. PostGIS
2. Cross Origin Resource Sharing
3. Usage example of Django REST Framework
4. JWT authentication with Django REST Framework
5. API documentation programming
6. Using cache with apiview and viewsets


<br>

### PostGIS

1. Create a django database model like following:

```python
# from django.db import models
from django.contrib.gis.db import models


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50, unique=True)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        """Representation in string.
        Returns:
            str: return a string like France (34.453, -8.9877)
        """
        return "{} ({}, {})".format(self.name, self.lat, self.lon)

```

> **NOTE**: If you use a spacial database, you must use `django.contrib.gis.db` inside of
> `django.db`.

2. Create a new file named `load.py` into your package application and write
the following source code:

```python
"""Data loading module.

.. _For more information on this file, see:
https://docs.djangoproject.com/en/4.1/ref/contrib/gis/tutorial/#layermapping
"""

from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import WorldBorder


WORLD_MAPPING = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'mpoly': 'MULTIPOLYGON',
}
WORLD_SHP = Path(__file__).resolve().parent / 'data'\
     / 'TM_WORLD_BORDERS-0.3.shp'


def run(verbose=True):
    """Function of data loading into database.

    Args:
        verbose (bool): Specifies if the loading process 
            will be verbose or not.
    """
    lm = LayerMapping(WorldBorder, WORLD_SHP, WORLD_MAPPING, transform=False)
    lm.save(strict=True, verbose=verbose)

```


### Cross Origin Resource Sharing (CORS)
You can define  a list of domains that will be allowed to access the resources of your server, by defining `CORS_ALLOWED_ORIGINS` variable in `server/core/settings.py` file as follows :

```python
# ...

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://192.168.9.102:3000',
]

```

The above setting will permit the server to allow all application hosted at 
`http://localhost:4200` and `http://192.168.9.102:3000` 
to access to resources of your server. By default, 
we have the following configuration is already defined :

```python
# ...

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

```

With this configuration, the server accepts all request from another any server.

### Usage example of Django REST Framework
You can insert directly the following source code in `server/core/urls.py` file :

```python
# ...


from django.urls import include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


# ...


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # ...
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
];

```

###  JWT authentication with Django REST Framework
We can use the  `JWT authentication` for all authentications in your API.
1. Installation :

```sh
pip install djangorestframework-simplejwt
```

2. Setting of `DEFAULT_AUTHENTICATION_CLASSES` to `JWTAuthentication` class.

```python
# REST framework settings
REST_FRAMEWORK = {
    # You can use JWT Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # ...

}

```

3. Then, you can configurate its functioning using the following source code that you will inserte 
   into `server/core/settings.py` file:

```python
from datetime import timedelta

# ...

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

```
4. Insert the following source code into `server/core/urls.py` 
for example, to use the authentication API that is already available 
by default in this package.

```python
# ...

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# ...

urlpatterns = [
    # ...
	
    # to get authentication tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # to refresh the access token using refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]
```

For more information, you can see the documentation 
of this package [here](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html).

### API documentation programming
The API documentations are generated by `drf_yasg` in **swagger** specification. This Django package is installed into this project by default. <br/>
So, given an Django application named `myapp` with its `serializers.py` module and let's consider the following usage example on an API view :

```python
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import response
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from myapp.serializers import UserSerializer


class UserAPI(viewsets.ViewSet):
    """Representation of the users API."""
    permission_classes = (permissions.IsAuthenticated,);

    # Here is the setting of API description in the documentation
    @swagger_auto_schema(
        operation_description=(
            "This method returns the user object that corresponds "
            "to the current user."
        ),
        responses={
            200: UserSerializer,
            400: "Bad request!",
            404: "Not Found!",
        }
    )
    def list(self, request):
        """Getting the list.

        Redefined function to perform our operation of user list
        retreiving.
        """
        user = User.objects.get(username=request.user)
        user_data = UserSerializer(user).data
        return response.Response(user_data)

```

> `swagger_auto_schema()` is used in decoration for `list()` function.
> - **operation_description** is used to give a description to this method.
> - **responses** is used to specify the different messages or returns
> for each server code.


### Using cache with apiview and viewsets
Django provides a `method_decorator` to use decorators
with class based views. This can be used with other cache
decorators such as `cache_page`, `vary_on_cookie` and `vary_on_headers`.

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.forms import model_to_dict

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


class UserViewSet(viewsets.ViewSet):
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
        content = {
            'user_feed': model_to_dict(request.user)
        }
        return Response(content)


class ProfileView(APIView):
    # With auth: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, format=None):
        content = {
            'user_feed': model_to_dict(request.user)
        };
        return Response(content)


class PostView(APIView):
    # Cache page for the requested url
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        content = {
            'title': 'Post title',
            'body': 'Post content'
        }
        return Response(content)

```

> **NOTE** : The `cache_page` decorator only 
> caches the `GET` and `HEAD` responses with `status 200`.

### Hosting

```sh
openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out path_to_certificate.crt -keyout path_to_private_key.key
```

```conf
server {
    root /home/mokira3d48/cobra/;
    listen              443 ssl;
    server_name         cobra.com;
    # server_name         ip_address;
    keepalive_timeout   70;

    ssl_certificate     /path_to_certificate.crt;
    ssl_certificate_key /path_to_private_key.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
        
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8000;
    }
        
}
```

<br/>


