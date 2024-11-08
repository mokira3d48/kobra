Django fournit un système de gestion des sessions qui vous permet de stocker
et de récupérer des données utilisateur entre différentes requêtes.
Les sessions sont utiles pour conserver des informations temporaires
propres à chaque utilisateur, comme un panier d'achat ou les préférences
d'affichage.

Voici les principales opérations de manipulation des variables de session
dans Django :

### 1. Activer les sessions dans Django

Pour utiliser les sessions, assurez-vous d’avoir activé le middleware
des sessions dans votre fichier `settings.py` :

```python
# settings.py

MIDDLEWARE = [
    # Middlewares par défaut
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Middleware de session
    'django.middleware.common.CommonMiddleware',
    # Autres middlewares
]
```

### 2. Créer ou mettre à jour une variable de session

Vous pouvez créer ou mettre à jour une variable de session en assignant
une valeur dans `request.session` avec une clé spécifique.

```python
def set_session_data(request):
    # Définir une variable de session
    request.session['user_name'] = 'John Doe'
    request.session['is_logged_in'] = True
    return HttpResponse("Les données de session ont été définies.")
```

Ici, la clé `'user_name'` est utilisée pour stocker le nom de l'utilisateur,
et `'is_logged_in'` pour indiquer si l'utilisateur est connecté.

### 3. Lire une variable de session

Pour lire une variable de session, utilisez la clé
avec `request.session.get()`. Si la clé n'existe pas, `get` retournera `None`
par défaut, ou une valeur de secours si vous la précisez.

```python
def get_session_data(request):
    user_name = request.session.get('user_name', 'Visiteur')
    is_logged_in = request.session.get('is_logged_in', False)
    return HttpResponse(f"Nom d'utilisateur : {user_name}, Connecté : {is_logged_in}")
```

Dans cet exemple, si `'user_name'` n'est pas défini, `user_name` prendra
la valeur `'Visiteur'`.

### 4. Supprimer une variable de session

Pour supprimer une variable spécifique de la session, utilisez `del`
avec la clé correspondante.

```python
def delete_session_data(request):
    try:
        del request.session['user_name']
    except KeyError:
        pass  # Si la clé n'existe pas, on ignore l'exception
    return HttpResponse("La variable de session 'user_name' a été supprimée.")
```

Ici, on utilise un bloc `try-except` pour éviter une erreur
si la clé n'existe pas.

### 5. Effacer toutes les données de session

Pour supprimer toutes les données de session pour un utilisateur spécifique,
utilisez la méthode `flush()`. Cela supprime toutes les variables de session
et réinitialise la session.

```python
def clear_session(request):
    request.session.flush()
    return HttpResponse("Toutes les données de session ont été effacées.")
```

**Note** : `flush()` supprime également le cookie de session,
donc une nouvelle session sera créée pour le prochain accès de cet utilisateur.

### 6. Spécifier la durée de vie des sessions

Django supprime automatiquement les sessions inactives après un certain
temps (par défaut, 2 semaines). Vous pouvez ajuster
cette durée de vie dans `settings.py` avec le paramètre `SESSION_COOKIE_AGE`
(en secondes).

```python
# settings.py

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 semaine (en secondes)
```

Vous pouvez également rendre la session "transitoire" (elle se termine lorsque
l'utilisateur ferme le navigateur) en activant
`SESSION_EXPIRE_AT_BROWSER_CLOSE` :

```python
# settings.py

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

### 7. Marquer la session comme modifiée

Parfois, Django ne détecte pas automatiquement les modifications de session.
Dans ce cas, vous pouvez utiliser `request.session.modified = True`
pour forcer Django à enregistrer les changements dans la session.

```python
def update_session_data(request):
    request.session['user_name'] = 'Jane Doe'
    request.session.modified = True  # Forcer la sauvegarde des modifications
    return HttpResponse("Les données de session ont été mises à jour.")
```

### 8. Autres configurations de session

Dans `settings.py`, vous pouvez également définir d'autres configurations
de session, comme :

- `SESSION_ENGINE` : pour changer le backend de session (ex. : cookies, cache, 
    fichiers).
- `SESSION_COOKIE_NAME` : pour changer le nom du cookie de session.
- `SESSION_SAVE_EVERY_REQUEST` : pour sauvegarder la session à chaque requête
(utile pour prolonger la durée de vie d’une session active).

### Exemple complet

Voici un exemple qui montre plusieurs manipulations de session
dans une vue Django :

```python
from django.http import HttpResponse

def session_example(request):
    # Initialiser ou mettre à jour une variable de session
    request.session['visit_count'] = request.session.get('visit_count', 0) + 1

    # Lire la variable de session
    visit_count = request.session['visit_count']

    # Supprimer la variable si elle dépasse un certain seuil
    if visit_count > 10:
        del request.session['visit_count']
        return HttpResponse("Le compteur a été réinitialisé après 10 visites.")
    
    return HttpResponse(f"Nombre de visites : {visit_count}")
```

Les sessions sont un moyen flexible de stocker des données propres
aux utilisateurs dans Django. Vous pouvez facilement définir, lire,
mettre à jour et supprimer des variables de session selon vos besoins.
