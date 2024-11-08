# Modeles Django

## Introduction
Pour réaliser des requêtes avec les modèles Django, vous utilisez l'API ORM (Object-Relational Mapping) fournie par Django. Cette API vous permet d'interagir avec la base de données de manière intuitive en utilisant des objets Python. Voici un guide détaillé sur la manière de réaliser des requêtes avec les modèles Django.

### 1. Configuration du Modèle

Avant de faire des requêtes, vous devez définir vos modèles. Voici un exemple simple d'un modèle `Article` :

```python
# models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### 2. Accéder au Shell Django

Pour expérimenter avec les requêtes, ouvrez le shell Django :

```bash
python manage.py shell
```

### 3. Importer le Modèle

Dans le shell, commencez par importer votre modèle :

```python
from myapp.models import Article  # Remplacez 'myapp' par le nom de votre application
```

### 4. Requêtes de Base

Voici quelques requêtes de base que vous pouvez effectuer :

- **Récupérer tous les objets** :

```python
articles = Article.objects.all()  # Récupère tous les articles
```

- **Récupérer un objet par clé primaire** :

```python
article = Article.objects.get(pk=1)  # Récupère l'article avec l'ID 1
```

- **Filtrer les objets** :

```python
filtered_articles = Article.objects.filter(title__contains="Django")  # Articles dont le titre contient "Django"
```

- **Exclure des objets** :

```python
excluded_articles = Article.objects.exclude(title__contains="Django")  # Articles dont le titre ne contient pas "Django"
```

### 5. Requêtes Avancées

Vous pouvez également effectuer des requêtes plus complexes en utilisant des filtres combinés et des expressions Q.

- **Combiner des filtres** :

```python
from django.db.models import Q

# Articles publiés après une certaine date et dont le titre contient "Django"
articles = Article.objects.filter(pub_date__gt='2023-01-01').filter(title__icontains='Django')
```

- **Utiliser Q pour des requêtes complexes** :

```python
# Articles dont le titre contient "Django" ou "Python"
articles = Article.objects.filter(Q(title__icontains='Django') | Q(title__icontains='Python'))
```

### 6. Tri et Limitation des Résultats

Vous pouvez trier les résultats et limiter le nombre d'objets retournés.

- **Trier les résultats** :

```python
sorted_articles = Article.objects.all().order_by('-pub_date')  # Articles triés par date de publication décroissante
```

- **Limiter le nombre de résultats** :

```python
limited_articles = Article.objects.all()[:5]  # Récupère les 5 premiers articles
```

### 7. Agrégation et Annotation

Django ORM permet également d'effectuer des opérations d'agrégation sur vos données.

- **Compter les articles** :

```python
from django.db.models import Count

article_count = Article.objects.count()  # Compte le nombre total d'articles
```

- **Calculer des moyennes, sommes, etc.** :

```python
from django.db.models import Avg

average_length = Article.objects.aggregate(Avg('content_length'))  # Exemple pour calculer la longueur moyenne du contenu (si vous avez un champ pour ça)
```

En utilisant l'ORM de Django, vous pouvez facilement réaliser des requêtes complexes sur vos modèles sans avoir à écrire directement du SQL. Cela rend la manipulation des données intuitive et maintient votre code propre et lisible. Pour plus d'informations détaillées sur les requêtes dans Django, consultez la [documentation officielle](https://docs.djangoproject.com/en/stable/topics/db/queries/).

### References

- [1] https://www.aiprm.com/fr/prompts/softwareengineering/backend-development/1904757701952151552/
- [2] http://www.python-simple.com/python-django-developpement-web/django-queryset.php
- [3] https://zestedesavoir.com/tutoriels/598/developpez-votre-site-web-avec-le-framework-django/264_techniques-avancees/1528_techniques-avancees-dans-les-modeles/
- [4] https://docs.djangoproject.com/fr/5.1/topics/db/models/
- [5] https://djangospirit.readthedocs.io/en/latest/topics/db/queries.html
- [6] https://docs.djangoproject.com/fr/5.1/topics/db/optimization/
- [7] https://docs.djangoproject.com/fr/5.1/topics/db/queries/

## Niveau intermediaire
Pour réaliser des requêtes avancées avec les modèles Django, vous pouvez utiliser plusieurs fonctionnalités puissantes fournies par l'ORM de Django. Voici un aperçu des concepts clés et des exemples pratiques pour effectuer des requêtes complexes.

### 1. Utilisation des Objets Q

Les objets `Q` vous permettent de créer des requêtes complexes en combinant des conditions avec des opérateurs logiques (`AND`, `OR`, `NOT`). Cela est particulièrement utile lorsque vous devez filtrer des objets en fonction de plusieurs critères.

#### Exemple d'utilisation de Q

```python
from django.db.models import Q
from myapp.models import Product

# Récupérer tous les produits dont le nom est 'phone' et le prix est supérieur à 500,
# ou dont le nom est 'tablet' et le prix est inférieur à 400.
products = Product.objects.filter(
    Q(name='phone', price__gt=500) | Q(name='tablet', price__lt=400)
)
```

### 2. Filtrage Avancé

Vous pouvez utiliser plusieurs filtres pour affiner vos requêtes. Par exemple, pour récupérer les articles publiés après une certaine date et dont le titre contient un mot spécifique :

```python
from myapp.models import Article

# Récupérer les articles publiés après le 1er janvier 2023 et dont le titre contient "Django"
articles = Article.objects.filter(pub_date__gt='2023-01-01', title__icontains='Django')
```

### 3. Utilisation de `select_related` et `prefetch_related`

Ces méthodes sont utilisées pour optimiser les requêtes en réduisant le nombre de requêtes SQL nécessaires pour récupérer des objets liés.

- **`select_related`** : Utilisé pour suivre les relations de clé étrangère. Cela effectue une jointure SQL.

```python
# Récupérer tous les livres avec leurs auteurs en une seule requête
books = Book.objects.select_related('author').all()
```

- **`prefetch_related`** : Utilisé pour récupérer des relations de type "many-to-many" ou "reverse foreign key". Cela effectue une requête séparée pour chaque relation.

```python
# Récupérer toutes les commandes avec leurs produits associés
orders = Order.objects.prefetch_related('product_set').all()
```

### 4. Agrégation et Annotation

Django permet d'effectuer des opérations d'agrégation sur vos données, comme compter, calculer la moyenne, etc.

#### Exemple d'Agrégation

```python
from django.db.models import Count, Avg

# Compter le nombre total d'articles
article_count = Article.objects.aggregate(total=Count('id'))

# Calculer la moyenne du prix des produits
average_price = Product.objects.aggregate(avg_price=Avg('price'))
```

### 5. Utilisation de `values()` et `values_list()`

Ces méthodes vous permettent de récupérer uniquement certains champs au lieu de récupérer tous les champs d'un modèle. Cela peut améliorer les performances en réduisant la quantité de données chargées.

#### Exemple avec `values()`

```python
# Récupérer uniquement les titres et les dates de publication des articles
article_data = Article.objects.values('title', 'pub_date')
for article in article_data:
    print(article['title'], article['pub_date'])
```

#### Exemple avec `values_list()`

```python
# Récupérer une liste de tuples contenant uniquement les titres et les prix des produits
product_data = Product.objects.values_list('title', 'price')
for title, price in product_data:
    print(title, price)
```

### 6. Définir des Conditions Dynamiques

Vous pouvez également créer des conditions dynamiques en utilisant Python standard, ce qui est utile lorsque vous construisez des requêtes basées sur l'entrée utilisateur.

#### Exemple d'utilisation dynamique

```python
import operator
from django.db.models import Q
from functools import reduce

conditions = [
    Q(name__startswith='A'),
    Q(price__lt=100)
]

# Combiner les conditions avec OR
queryset = Product.objects.filter(reduce(operator.or_, conditions))
```

Avec ces techniques avancées, vous pouvez tirer parti de la puissance de l'ORM Django pour effectuer des requêtes complexes et optimisées sur vos modèles. L'utilisation d'objets `Q`, d'agrégations, de préchargements, et de méthodes comme `values()` et `values_list()` vous permet d'écrire des requêtes efficaces tout en maintenant un code clair et lisible. Pour plus d'informations détaillées sur ces fonctionnalités, consultez la [documentation officielle de Django](https://docs.djangoproject.com/en/stable/topics/db/queries/).

## References

- [1] https://micropyramid.com/blog/querying-with-django-q-objects
- [2] https://www.linkedin.com/pulse/optimizing-djangos-queryset-performance-advanced-rashid-mahmood
- [3] https://python.plainenglish.io/master-django-orm-advanced-concepts-2b4fce773f4e?gi=7763a5d258ed
- [4] https://dev.to/krystianmaccs/django-complex-query-methods-a75
