# Les fixtures

## Introduction
Certainement. Je vais vous expliquer en détail le fonctionnement des fixtures
et comment les utiliser spécifiquement avec Django pour tester une API REST.

1. Concept des fixtures dans Django

Les fixtures dans Django sont des fichiers contenant des données initiales
pour la base de données. Elles sont utilisées pour pré-remplir la base
de données avec un ensemble connu de données, ce qui est particulièrement
utile pour les tests.

2. Format des fixtures

Les fixtures dans Django sont généralement écrites en JSON ou YAML.
Voici un exemple de fixture en JSON :



```json
[
  {
    "model": "myapp.author",
    "pk": 1,
    "fields": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  },
  {
    "model": "myapp.book",
    "pk": 1,
    "fields": {
      "title": "Django for Beginners",
      "author": 1,
      "publication_date": "2023-01-01"
    }
  }
]

```

3. Création des fixtures

Vous pouvez créer des fixtures manuellement ou les générer à partir de données existantes :

```bash
python manage.py dumpdata myapp.author myapp.book > myapp/fixtures/initial_data.json
```

4. Emplacement des fixtures

Placez vos fichiers de fixtures dans un dossier nommé `fixtures`
à l'intérieur de votre application Django.

5. Chargement des fixtures

Pour charger les fixtures, utilisez la commande :

```bash
python manage.py loaddata myapp/fixtures/initial_data.json
```

6. Utilisation des fixtures dans les tests

Voici comment utiliser les fixtures dans vos tests Django pour une API REST :



```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from myapp.models import Author, Book


class BookAPITestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = APIClient()

    def test_get_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')

    def test_get_book_detail(self):
        book = Book.objects.first()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')
        self.assertEqual(response.data['author']['name'], 'John Doe')

```

Dans cet exemple :
- Nous spécifions les fixtures à utiliser
avec `fixtures = ['initial_data.json']`.
- `setUp` initialise le client API pour chaque test.
- Nous testons à la fois la liste des livres et les détails d'un livre.

7. Fixtures et authentification

Pour tester des endpoints nécessitant une authentification :

```python
from django.contrib.auth.models import User

class AuthenticatedAPITestCase(TestCase):
    fixtures = ['users.json', 'books.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username='testuser')
        self.client.force_authenticate(user=self.user)

    def test_create_book(self):
        url = reverse('book-list')
        data = {'title': 'New Book', 'author': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

8. Utilisation de factory boy avec Django REST framework

Pour des scénarios de test plus dynamiques, vous pouvez combiner
les fixtures avec `factory_boy` :

```python
import factory
from myapp.models import Author, Book

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    name = factory.Faker('name')
    email = factory.Faker('email')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    title = factory.Faker('sentence')
    author = factory.SubFactory(AuthorFactory)
    publication_date = factory.Faker('date_this_decade')

# Dans vos tests
def setUp(self):
    self.author = AuthorFactory()
    self.book = BookFactory(author=self.author)
```

9. Gestion des fixtures dans les tests

- Utilisez `setUpTestData` pour charger des données une seule fois
pour toute la classe de test :

```python
class LargeDatasetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Chargez ici vos données volumineuses
        call_command('loaddata', 'large_dataset.json')
```

10. Bonnes pratiques pour l'utilisation des fixtures dans les tests Django REST

- Gardez vos fixtures légères et spécifiques à chaque test.
- Utilisez des noms descriptifs pour vos fichiers de fixtures.
- Préférez les factory boys pour les données dynamiques et les fixtures pour les données statiques.
- Assurez-vous que vos fixtures sont à jour avec votre schéma de base de données.
- Utilisez des fixtures différentes pour tester différents scénarios (par exemple, utilisateurs avec différents rôles).

11. Gestion des relations dans les fixtures

Pour les modèles avec des relations, assurez-vous que vos fixtures maintiennent l'intégrité référentielle :

```json
[
  {
    "model": "myapp.author",
    "pk": 1,
    "fields": {
      "name": "Jane Doe",
      "email": "jane@example.com"
    }
  },
  {
    "model": "myapp.book",
    "pk": 1,
    "fields": {
      "title": "Advanced Django",
      "author": 1,
      "genres": [1, 2]
    }
  },
  {
    "model": "myapp.genre",
    "pk": 1,
    "fields": {
      "name": "Programming"
    }
  },
  {
    "model": "myapp.genre",
    "pk": 2,
    "fields": {
      "name": "Web Development"
    }
  }
]
```

12. Utilisation de fixtures pour les tests de performance

Pour tester les performances de votre API avec un grand volume de données :

```python
class PerformanceTestCase(TestCase):
    fixtures = ['large_dataset.json']

    def test_book_list_performance(self):
        url = reverse('book-list')
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        self.assertLess(end_time - start_time, 1.0)
        #: Le temps de réponse doit être inférieur à 1 seconde
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

En conclusion, les fixtures sont un outil puissant pour créer
des environnements de test reproductibles et fiables dans Django,
particulièrement pour tester des API REST. En les combinant
avec les outils de test de Django REST framework comme APIClient,
vous pouvez créer des suites de tests robustes qui couvrent tous les aspects
de votre API.
