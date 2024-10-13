# Celery

## Introduction
Celery est une bibliothèque Python conçue pour exécuter des tâches
asynchrones et planifiées, facilitant ainsi la gestion des tâches
en arrière-plan dans les applications. Voici une explication détaillée
de son fonctionnement, de sa configuration à son utilisation.

### 1. Architecture de Celery

Celery repose sur une architecture client-serveur, où les tâches
sont envoyées à un courtier de messages (message broker) qui gère
la distribution des tâches aux workers (travailleurs).

#### Composants principaux :

- **Tâches** : Ce sont les fonctions que vous souhaitez exécuter
de manière asynchrone.
  
- **Courrier de messages** : Celery utilise un système de messagerie
pour communiquer entre le client et les workers. Les courtiers populaires
incluent RabbitMQ, Redis, et Amazon SQS.

- **Workers** : Ce sont les processus qui exécutent les tâches.
Vous pouvez avoir plusieurs workers pour gérer les tâches simultanément.

### 2. Installation de Celery

Pour installer Celery, utilisez pip :

```bash
pip install celery
```

### 3. Configuration de Celery

Vous devez configurer Celery dans votre application (par exemple,
une application Django). Voici un exemple de configuration :

#### Exemple pour Django

1. **Créer le fichier de configuration** :

```python
# myapp/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

2. **Configurer le courtier de messages** :

Dans votre `settings.py`, configurez le courtier :

```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Exemple avec Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Pour stocker les résultats
```

### 4. Définition des Tâches

Les tâches sont définies comme des fonctions décorées avec `@shared_task`
ou `@app.task`. Voici un exemple :

```python
# myapp/tasks.py
from celery import shared_task

@shared_task
def add(x, y):
    return x + y
```

### 5. Appel des Tâches

Pour appeler une tâche, utilisez la méthode `delay()` ou `apply_async()` :

```python
# Appel asynchrone
result = add.delay(4, 6)

# Ou avec apply_async pour plus d'options
result = add.apply_async((4, 6), countdown=10)  # Exécute après 10 secondes
```

### 6. Gestion des Résultats

Celery peut également gérer les résultats des tâches. Pour cela,
vous devez configurer un backend pour stocker les résultats
(comme Redis ou une base de données).

```python
# settings.py
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

Vous pouvez récupérer le résultat d'une tâche comme suit :

```python
if result.ready():
    print(result.result)  # Affiche le résultat si la tâche est terminée
```

### 7. Planification des Tâches

Celery permet également la planification des tâches à l'aide de Celery Beat,
qui est un scheduler intégré.

#### Exemple de planification :

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'myapp.tasks.add',
        'schedule': 30.0,
        'args': (16, 16),
    },
}
```

### 8. Démarrer Celery

Pour démarrer le worker et le scheduler, utilisez les commandes suivantes
dans votre terminal :

```bash
# Démarrer le worker
celery -A myapp worker --loglevel=info

# Démarrer le scheduler (Beat)
celery -A myapp beat --loglevel=info
```

### 9. Monitoring et Gestion des Workers

Celery fournit également des outils pour surveiller l'état des workers
et des tâches en cours d'exécution.

- **Flower** : Un outil web pour surveiller et administrer vos workers Celery.
  
Pour l'installer :

```bash
pip install flower
```

Pour le démarrer :

```bash
celery -A myapp flower
```

Celery est un outil puissant pour gérer l'exécution asynchrone
et la planification des tâches dans vos applications Python.
En déchargeant les tâches lourdes vers des workers en arrière-plan,
vous améliorez la réactivité et l'évolutivité de votre application.
Pour plus d'informations détaillées, consultez la [documentation officielle de Celery](https://docs.celeryproject.org/en/stable/index.html).


## Principals composents de Celery
Celery est un outil puissant pour exécuter des tâches asynchrones
dans des applications Python. Voici les principaux composants de Celery
et leur fonctionnement :

### 1. Tâches (Tasks)

Les **tâches** sont des fonctions que vous souhaitez exécuter de manière
asynchrone. Elles sont généralement définies à l'aide du décorateur
`@shared_task` ou `@app.task`. Chaque tâche peut avoir un identifiant
unique et un état (en attente, en cours d'exécution, terminé, échoué).

**Exemple de définition d'une tâche :**

```python
from celery import shared_task

@shared_task
def add(x, y):
    return x + y
```

### 2. Workers

Les **workers** sont des processus qui exécutent les tâches en arrière-plan.
Ils se connectent au courtier de messages pour récupérer les tâches à exécuter.
Vous pouvez avoir plusieurs workers pour traiter plusieurs tâches
simultanément.

**Démarrer un worker :**

```bash
celery -A myapp worker --loglevel=info
```

### 3. Courrier de Messages (Message Broker)

Le **courrier de messages** est un composant essentiel qui fait
le lien entre le client (l'application qui envoie les tâches) et les workers
(qui exécutent les tâches). Le courtier gère la file d'attente des tâches
et permet aux workers de récupérer ces tâches.

Les courtiers populaires incluent :
- **RabbitMQ**
- **Redis**
- **Amazon SQS**

**Configuration d'un courtier dans Django :**

```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
```

### 4. Backend de Résultats (Result Backend)

Le **backend de résultats** est utilisé pour stocker les résultats des tâches
exécutées. Cela permet à l'application de récupérer le résultat d'une tâche
après son exécution.

**Configuration d'un backend de résultats :**

```python
# settings.py
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

### 5. Application Celery (Celery App)

L'**application Celery** est une instance de Celery qui regroupe
la configuration et les tâches. Elle est utilisée pour définir le comportement
global de votre application Celery.

**Exemple de création d'une application Celery :**

```python
from celery import Celery

app = Celery('myapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### 6. Scheduler (Celery Beat)

**Celery Beat** est un scheduler intégré qui permet de planifier l'exécution
périodique des tâches. Il fonctionne en parallèle avec les workers
et permet d'exécuter des tâches à intervalles réguliers.

**Exemple de configuration d'une tâche planifiée :**

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'myapp.tasks.add',
        'schedule': 30.0,
        'args': (16, 16),
    },
}
```

### 7. Monitoring

Pour surveiller l'état des workers et des tâches, vous pouvez utiliser
des outils comme **Flower**, qui fournit une interface web pour visualiser
l'activité des workers et les résultats des tâches.

**Installation et démarrage de Flower :**

```bash
pip install flower
celery -A myapp flower
```

Celery est un système robuste pour gérer l'exécution asynchrone
et la planification des tâches dans vos applications Python.
En utilisant ses composants tels que les tâches, les workers, le courtier
de messages et le backend de résultats, vous pouvez améliorer la réactivité
et l'évolutivité de votre application. Pour plus d'informations détaillées,
consultez la [documentation officielle de Celery](https://docs.celeryproject.org/en/stable/index.html).

### Références

[1] https://vkaustubh.github.io/blog/geek/2019-12-17-introduction-to-celery.html
[2] https://stackoverflow.com/questions/42638206/celery-understanding-the-big-picture


