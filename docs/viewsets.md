## API Viewset
Pour créer une API utilisant un `ViewSet` et le `DefaultRouter`
dans Django REST Framework, suivez les étapes ci-dessous.
Cet exemple illustrera comment configurer un modèle, un sérialiseur,
un `ViewSet`, et les routes.

### Étapes pour créer l'API

1. **Définir le modèle** : Créez un modèle pour représenter les données.
2. **Créer le sérialiseur** : Créez un sérialiseur pour le modèle.
3. **Créer le ViewSet** : Créez un `ViewSet` pour gérer les opérations CRUD.
4. **Configurer les routes avec DefaultRouter** : Enregistrez le `ViewSet`
avec le `DefaultRouter`.

### Exemple de code

#### 1. Définir le modèle

Commençons par définir un modèle simple, par exemple, un modèle `Book`.

```python
# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title
```

#### 2. Créer le sérialiseur

Ensuite, créons un sérialiseur pour le modèle `Book`.

```python
# serializers.py
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']
```

#### 3. Créer le ViewSet

Maintenant, nous allons créer un `ViewSet` pour gérer les opérations
CRUD sur les livres.

```python
# views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

#### 4. Configurer les routes avec DefaultRouter

Enfin, configurons les routes dans `urls.py` en utilisant `DefaultRouter`.

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    #: Inclut toutes les routes générées par le router
]
```

### Explications des routes générées

Avec cette configuration, le `DefaultRouter` génère automatiquement
les routes suivantes pour le `BookViewSet` :

- **GET /books/** : Lister tous les livres (méthode `list`).
- **POST /books/** : Créer un nouveau livre (méthode `create`).
- **GET /books/{id}/** : Récupérer un livre spécifique (méthode `retrieve`).
- **PUT /books/{id}/** : Mettre à jour un livre existant (méthode `update`).
- **PATCH /books/{id}/** : Mettre à jour partiellement un livre existant
(méthode `partial_update`).
- **DELETE /books/{id}/** : Supprimer un livre (méthode `destroy`).

En suivant ces étapes, vous avez créé une API simple utilisant
Django REST Framework avec un `ViewSet` et un `DefaultRouter`.
Cela vous permet de gérer facilement les opérations CRUD sur votre modèle
tout en maintenant une structure d'URL cohérente et propre. Pour plus
de détails sur l'utilisation des ViewSets et des routers,
consultez la [documentation officielle de Django REST Framework](https://www.django-rest-framework.org/api-guide/viewsets/).

### Références
- [1] https://stackoverflow.com/questions/69858780/how-to-route-to-specific-viewset-methods-django
- [2] https://testdriven.io/blog/drf-views-part-3/
- [3] https://python.plainenglish.io/simplified-url-routing-in-django-rest-framework-23a344ca1b4d?gi=04999100eddf
- [4] https://github.com/encode/django-rest-framework/discussions/7830
- [5] https://forum.djangoproject.com/t/django-rest-framework-viewsets-urls/6413
- [6] https://www.django-rest-framework.org/api-guide/viewsets/
- [7] https://www.django-rest-framework.org/api-guide/routers/
- [8] https://pytest-django.readthedocs.io/en/latest/helpers.html


## Nom de routes
Lorsque vous utilisez un `ViewSet` avec le `DefaultRouter`
dans Django REST Framework, plusieurs routes sont automatiquement
générées. Voici les noms de route qui sont généralement
créés pour un `ViewSet` :

### Noms de route générés par un ViewSet

1. **List** : 
   - **URL** : `/books/`
   - **Nom** : `book-list`
   - **Méthode HTTP** : `GET`
   - **Description** : Récupérer une liste de tous les livres.

2. **Create** :
   - **URL** : `/books/`
   - **Nom** : `book-create`
   - **Méthode HTTP** : `POST`
   - **Description** : Créer un nouveau livre.

3. **Retrieve** :
   - **URL** : `/books/{id}/`
   - **Nom** : `book-detail`
   - **Méthode HTTP** : `GET`
   - **Description** : Récupérer un livre spécifique par son ID.

4. **Update** :
   - **URL** : `/books/{id}/`
   - **Nom** : `book-update`
   - **Méthode HTTP** : `PUT`
   - **Description** : Mettre à jour un livre existant par son ID.

5. **Partial Update** :
   - **URL** : `/books/{id}/`
   - **Nom** : `book-partial-update`
   - **Méthode HTTP** : `PATCH`
   - **Description** : Mettre à jour partiellement un livre existant
par son ID.

6. **Destroy** :
   - **URL** : `/books/{id}/`
   - **Nom** : `book-delete`
   - **Méthode HTTP** : `DELETE`
   - **Description** : Supprimer un livre par son ID.

### Exemple d'enregistrement d'un ViewSet avec DefaultRouter

Voici comment vous pourriez configurer cela dans votre fichier `urls.py` :

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    #: Inclut toutes les routes générées par le router
]
```

En utilisant un `ViewSet` avec le `DefaultRouter`, vous bénéficiez
d'une gestion automatique des routes pour les opérations CRUD,
ce qui simplifie considérablement la configuration des URL
dans votre API Django REST Framework. Les noms de route générés peuvent
être utilisés pour référencer ces routes dans vos templates
ou dans d'autres parties de votre code Django.

### Références
- [1] https://makina-corpus.com/logiciel-libre/generer-urls-django-partir-structure-dossiers
- [2] https://makina-corpus.com/django/django-rest-framework-fonctionnement-des-routeurs-partie-3
- [3] https://docs.djangoproject.com/fr/5.1/topics/http/urls/
- [4] https://www.univ-orleans.fr/iut-orleans/informatique/intra/tuto/django/django-routes-views.html
- [5] https://docs.djangoproject.com/fr/5.1/intro/tutorial01/
- [6] https://testdriven.io/blog/drf-views-part-3/
- [7] https://docs.djangoproject.com/fr/5.1/ref/urlresolvers/
- [8] https://stackoverflow.com/questions/69858780/how-to-route-to-specific-viewset-methods-django

