# Transaction

## Introduction
Pour réaliser des requêtes transactionnelles avec Django,
vous pouvez utiliser le décorateur ou le gestionnaire de contexte
`transaction.atomic()`. Cela vous permet de regrouper plusieurs opérations
de base de données dans une seule transaction, garantissant
ainsi que toutes les opérations réussissent ou qu'aucune ne soit appliquée
en cas d'erreur. Voici comment procéder :


### 1. Importer le Module

Commencez par importer le module `transaction` depuis `django.db`.

```python
from django.db import transaction
```

### 2. Utiliser `transaction.atomic()` comme Décorateur

Vous pouvez appliquer le décorateur `@transaction.atomic`
à une vue ou à une fonction pour exécuter tout le code à l'intérieur
d'une transaction.

**Exemple** :

```python
from django.http import HttpResponse
from django.db import transaction

@transaction.atomic
def create_user_and_profile(request):
    # Créez un nouvel utilisateur
    user = User.objects.create(username='new_user', password='password123')
    
    # Créez un profil associé à l'utilisateur
    profile = Profile.objects.create(user=user, bio='Hello, world!')

    return HttpResponse("User and profile created successfully!")
```

Dans cet exemple, si la création de l'utilisateur échoue, la création
du profil ne sera pas appliquée, et vice versa.

### 3. Utiliser `transaction.atomic()` comme Gestionnaire de Contexte

Vous pouvez également utiliser `transaction.atomic()` comme gestionnaire
de contexte pour des blocs de code spécifiques.

**Exemple** :

```python
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import transaction

User = get_user_model()


def update_user_profile(request, user_id):
    user = User.objects.get(id=user_id)

    with transaction.atomic():
        # Mettez à jour des informations sur l'utilisateur
        user.email = 'new_email@example.com'
        user.save()

        # Supposons que vous ayez une logique qui pourrait échouer ici
        if some_condition_fails:
            raise ValueError("Something went wrong!")

        # Mettez à jour le profil de l'utilisateur
        profile = user.profile
        profile.bio = 'Updated bio'
        profile.save()

    return HttpResponse("User profile updated successfully!")
```

### 4. Gérer les Exceptions

Vous pouvez également gérer les exceptions dans un bloc `try/except`
pour effectuer des opérations supplémentaires en cas d'erreur.

**Exemple** :

```python
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from .models import Profile

User = get_user_model()


@transaction.atomic
def create_user_with_error_handling(request):
    try:
        user = User.objects.create(username='another_user',
                                   password='password123')
        
        # Une opération qui pourrait échouer
        profile = Profile.objects.create(user=user, bio='This will fail if username is taken.')

    except IntegrityError:
        return HttpResponse("Failed to create user or profile due to integrity error.")

    return HttpResponse("User created successfully!")
```

### 5. Utiliser des Savepoints

Django permet également d'utiliser des savepoints pour gérer des transactions
imbriquées. Cela peut être utile si vous souhaitez effectuer un rollback
partiel.

**Exemple** :

```python
from django.db import transaction

def complex_operation(request):
    with transaction.atomic():  # Outer atomic block
        operation1()  # This will be committed if successful
        
        try:
            with transaction.atomic():  # Inner atomic block (savepoint)
                operation2()  # If this fails, only this operation will be rolled back
                operation3()
        
        except Exception:
            # Handle the exception for the inner block without affecting operation1
            pass

    return HttpResponse("Complex operation completed.")
```

En utilisant `transaction.atomic()`, vous pouvez facilement gérer
les transactions dans Django pour garantir l'intégrité des données.
Que vous choisissiez d'utiliser ce décorateur ou ce gestionnaire de contexte,
cela vous permet de contrôler précisément quand les modifications
sont appliquées à la base de données. Pour plus d'informations détaillées
sur la gestion des transactions dans Django, consultez
la [documentation officielle](https://docs.djangoproject.com/en/stable/topics/db/transactions/).

### References
- [1] https://docs.djangoproject.com/en/5.1/topics/db/transactions/
- [2] https://www.scaler.com/topics/django/django-transactions/
