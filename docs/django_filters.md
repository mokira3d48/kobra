# Django Filter

## Introduction
Les filtres sont un moyen puissant de permettre aux clients de l'API
de filtrer les résultats des requêtes en fonction de certains critères.

### 1. Concept de base

Django REST Framework offre plusieurs options
pour filtrer les résultats de l'API :

- FilterSets
- Generic Filtering
- DjangoFilterBackend
- SearchFilter
- OrderingFilter

Concentrons-nous sur les `FilterSets` et `DjangoFilterBackend`,
qui sont les plus couramment utilisés.

### 2. Installation

Tout d'abord, assurez-vous d'avoir installé `django-filter` :

```
pip install django-filter
```

Ajoutez-le à vos `INSTALLED_APPS` dans `settings.py` :

```python
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]
```

### 3. Configuration de base

Dans votre fichier `views.py` :


```python
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'genre']

```

Dans cet exemple, nous utilisons DjangoFilterBackend et spécifions
les champs sur lesquels nous voulons permettre le filtrage
avec `filterset_fields`.

### 4. Utilisation des `FilterSets`

Pour un contrôle plus fin, vous pouvez utiliser FilterSet :

```python
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='lte')
    genre = django_filters.CharFilter(field_name='genre__name',
                                      lookup_expr='iexact')

    class Meta:
        model = Book
        fields = ['title', 'author', 'min_price', 'max_price', 'genre']

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

```

Dans cet exemple :

- 'title' utilise icontains pour une recherche insensible à la casse.
- 'min_price' et 'max_price' permettent de filtrer sur une plage de prix.
- 'genre' filtre sur le nom du genre (supposant une relation `ForeignKey`).

### 5. Fonctionnement interne

Lorsqu'une requête est faite à l'API, voici ce qui se passe :

1. DRF reçoit la requête et la passe à la vue.
2. La vue vérifie les filter_backends spécifiés.
3. Pour `DjangoFilterBackend`, il examine les paramètres de requête.
4. Il compare ces paramètres aux champs définis
dans `filterset_fields` ou `filterset_class`.
5. Pour chaque correspondance, il applique le filtre approprié au queryset.
6. Le queryset filtré est ensuite passé au *serializer* pour la réponse.

### 6. Types de filtres courants

- `ExactFilter` : correspond exactement à la valeur (par défaut).
- `CharFilter` : pour les champs de texte, peut utiliser `contains`,
`icontains`, etc.
- `NumberFilter` : pour les champs numériques.
- `DateTimeFilter` : pour les champs de date et heure.
- `BooleanFilter` : pour les champs booléens.

### 7. Lookup expressions

Les lookup expressions définissent comment le filtrage est effectué.
Quelques exemples :

- `'exact'` : correspondance exacte
- `'iexact'` : correspondance exacte insensible à la casse
- `'contains'` : contient la valeur
- `'icontains'` : contient la valeur, insensible à la casse
- `'gt'`, `'gte'`, `'lt'`, `'lte'` : comparaisons (greater than, less than,
etc.)
- `'startswith'`, `'endswith'` : commence par, se termine par

### 8. Personnalisation avancée

Vous pouvez créer des méthodes de filtrage personnalisées
dans votre `FilterSet` :

```python
class BookFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method='filter_by_category')

    def filter_by_category(self, queryset, name, value):
        return queryset.filter(genre__category__name=value)
```

### 9. Utilisation côté client

Les clients peuvent utiliser ces filtres en ajoutant des paramètres à l'URL :

```
GET /api/books/?title=django&min_price=20&max_price=50
```

Cette requête filtrerait les livres dont le titre contient "django"
et dont le prix est entre 20 et 50.

Les filtres Django avec DRF offrent une grande flexibilité
pour permettre aux clients de l'API de récupérer précisément
les données dont ils ont besoin, tout en gardant le contrôle côté serveur
sur ce qui peut être filtré et comment.

## Personnalisation des filtres
Je comprends que vous souhaitez approfondir le sujet des filtres Django
avec Django REST Framework. Je vais vous présenter quelques aspects
plus avancés et des cas d'utilisation plus complexes.

### 1. Filtres personnalisés complexes

Parfois, vous aurez besoin de filtres plus complexes qui ne correspondent
pas directement aux champs de votre modèle. Voici un exemple :

```python
import django_filters
from django.db.models import Q
from .models import Book


class BookFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_by_keyword')
    price_range = django_filters.CharFilter(method='filter_by_price_range')
    
    class Meta:
        model = Book
        fields = ['keyword', 'price_range']

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(author__name__icontains=value) |
            Q(genre__name__icontains=value)
        )

    def filter_by_price_range(self, queryset, name, value):
        try:
            min_price, max_price = map(float, value.split(','))
            return queryset.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            return queryset

```

Dans cet exemple :
- `filter_by_keyword` permet une recherche sur plusieurs champs à la fois.
- `filter_by_price_range` accepte une chaîne de caractères au format
"min,max" et filtre en conséquence.

### 2. Filtres dépendants

Parfois, vous voulez que certains filtres dépendent d'autres filtres.
Voici comment vous pourriez implémenter cela :


```python
import django_filters
from .models import Book, Author

class BookFilter(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(queryset=Author.objects.all())
    author_country = django_filters.CharFilter(
                            method='filter_by_author_country')

    class Meta:
        model = Book
        fields = ['author', 'author_country']

    def filter_by_author_country(self, queryset, name, value):
        author = self.form.cleaned_data.get('author')
        if author:
            return queryset.filter(author__country__iexact=value)
        return queryset

```

Dans cet exemple, le filtre `author_country` ne s'applique que si un auteur
a été sélectionné.

### 3. Filtres avec des choix dynamiques

Vous pouvez créer des filtres dont les choix sont générés dynamiquement :

```python
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    genre = django_filters.ChoiceFilter(choices=lambda: [
        (genre.id, genre.name) for genre in Genre.objects.all()
    ])

    class Meta:
        model = Book
        fields = ['genre']

```

### 4. Intégration avec DRF's `SearchFilter` et `OrderingFilter`

Vous pouvez combiner `DjangoFilterBackend` avec d'autres backends de DRF :

```python
from rest_framework import filters


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'price', 'publication_date']
```

### 5. Filtres côté base de données vs côté Python

Par défaut, `django-filter` applique les filtres au niveau
de la base de données. Cependant, vous pouvez spécifier `filter_overrides`
pour changer ce comportement :

```python
class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ['title']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'method': 'my_custom_filter'
                },
            },
        }

    def my_custom_filter(self, queryset, name, value):
        # Logique de filtrage personnalisée
        return [obj for obj in queryset if value.lower() in obj.title.lower()]
```

### 6. Performance et optimisation

Lorsque vous utilisez des filtres complexes, il est important de considérer
la performance. Utilisez `select_related()` et `prefetch_related()`
pour optimiser les requêtes :

```python
class BookList(generics.ListAPIView):
    queryset = Book.objects.all().select_related('author') \
                                 .prefetch_related('genres')
    # ...
```

### 7. Tests unitaires pour les filtres

N'oubliez pas d'écrire des tests pour vos filtres personnalisés :

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Book, Author

class BookFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author1 = Author.objects.create(name="Author 1", country="USA")
        self.author2 = Author.objects.create(name="Author 2", country="UK")
        self.book1 = Book.objects.create(title="Django for Beginners",
                                         author=self.author1, price=29.99)
        self.book2 = Book.objects.create(title="Advanced Python",
                                         author=self.author2, price=39.99)

    def test_filter_by_keyword(self):
        url = reverse('book-list') + '?keyword=Django'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Django for Beginners")

    def test_filter_by_price_range(self):
        url = reverse('book-list') + '?price_range=25,35'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Django for Beginners")

    def test_filter_by_author_country(self):
        url = reverse('book-list')
              + f'?author={self.author1.id}&author_country=USA'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Django for Beginners")

```

Ces exemples avancés montrent la flexibilité et la puissance
des filtres Django avec DRF. Ils vous permettent de créer des API robustes
et flexibles, capables de gérer des scénarios de filtrage complexes
tout en maintenant une bonne performance et une facilité d'utilisation
pour les clients de l'API.


## Annotation et agrégation

Comme vous n'avez pas spécifié un aspect particulier, nous allons choisir
un sujet avancé qui n'a pas encore été abordé en détail : l'utilisation
de filtres personnalisés avec des annotations et des agrégations Django.
Cela peut être très utile pour des scénarios de filtrage complexes impliquant
des calculs ou des relations multiples.

Voici un exemple détaillé :

```python
from django.db.models import Avg, Count, Q
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import Book, Review

class BookFilter(filters.FilterSet):
    min_rating = filters.NumberFilter(method='filter_by_min_rating')
    min_reviews = filters.NumberFilter(method='filter_by_min_reviews')
    popular_genre = filters.BooleanFilter(method='filter_by_popular_genre')

    class Meta:
        model = Book
        fields = ['min_rating', 'min_reviews', 'popular_genre']

    def filter_by_min_rating(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('reviews__rating')) \
                       .filter(avg_rating__gte=value)

    def filter_by_min_reviews(self, queryset, name, value):
        return queryset.annotate(review_count=Count('reviews')) \
                       .filter(review_count__gte=value)

    def filter_by_popular_genre(self, queryset, name, value):
        if value:
            popular_genres = Book.objects.values('genre').annotate(
                book_count=Count('id')
            ).order_by('-book_count')[:3].values_list('genre', flat=True)
            return queryset.filter(genre__in=popular_genres)
        return queryset

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        return queryset

```

Expliquons ce code en détail :

1. `filter_by_min_rating`:
   - Utilise `annotate` pour calculer la note moyenne de chaque livre.
   - Filtre ensuite les livres dont la note moyenne est supérieure
   ou égale à la valeur spécifiée.

2. `filter_by_min_reviews`:
   - Utilise `annotate` pour compter le nombre de critiques pour chaque livre.
   - Filtre les livres ayant au moins le nombre spécifié de critiques.

3. `filter_by_popular_genre`:
   - Si activé, ce filtre sélectionne les trois genres les plus populaires
   (basés sur le nombre de livres).
   - Retourne ensuite tous les livres appartenant à ces genres populaires.

4. Dans la vue `BookList`:
   - Nous surchargeons `get_queryset` pour ajouter des annotations par défaut
   à tous les livres.
   - Cela permet d'inclure la note moyenne et le nombre de critiques
   dans les résultats de l'API, même si les filtres ne sont pas appliqués.

Utilisation de ces filtres :

1. Pour obtenir les livres avec une note moyenne d'au moins 4 :
```
GET /api/books/?min_rating=4
```

2. Pour obtenir les livres avec au moins 10 critiques :
```
GET /api/books/?min_reviews=10
```

3. Pour obtenir les livres des genres les plus populaires :
```
GET /api/books/?popular_genre=true
```

4. Ces filtres peuvent être combinés :
```
GET /api/books/?min_rating=4&min_reviews=10&popular_genre=true
```

Points importants à noter :

1. Performance : Les annotations et agrégations peuvent être coûteuses
en termes de performance, surtout sur de grandes bases de données.
Il est important d'optimiser ces requêtes, peut-être en utilisant des index
de base de données appropriés.

2. Réutilisabilité : Ces filtres peuvent être réutilisés dans différentes
vues ou même dans différentes parties de votre application en dehors de l'API.

3. Flexibilité : Cette approche vous permet de créer des filtres
très puissants qui peuvent effectuer des calculs complexes sur vos données.

4. Maintenabilité : En séparant la logique de filtrage dans une classe
`FilterSet`, vous gardez votre code propre et facile à maintenir.

Cette approche avancée des filtres Django avec DRF vous permet de créer
des API très flexibles et puissantes, capables de gérer des scénarios
de filtrage complexes impliquant des calculs et des relations multiples.


