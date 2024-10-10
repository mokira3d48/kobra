# Uploader de fichier

## Modèle Django
Pour créer un modèle Django qui permet de stocker des fichiers uploadés (documents et images) avec des noms de fichiers basés sur la date et l'heure, vous pouvez utiliser une fonction personnalisée pour le paramètre `upload_to` du champ `FileField` ou `ImageField`. Voici comment procéder :

### Exemple de modèle Django

```python
from django.db import models
from datetime import datetime

def upload_path(_instance, filename):
    # Générer un nom de fichier basé sur la date et l'heure actuelles
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Concaténer le nom de fichier original avec le timestamp
    return f"uploads/{current_time}_{filename}"

class UploadedFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('document', 'Document'),
        ('image', 'Image'),
    ]

    title = models.CharField(max_length=255)  # Titre du fichier
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)  # Type de fichier
    file = models.FileField(upload_to=upload_path)  # Champ pour le fichier uploadé
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date d'upload

    def __str__(self):
        return f"{self.title} ({self.file_type})"
```

### Explications des éléments du code

1. **Fonction `upload_path`** :
   - Cette fonction est appelée chaque fois qu'un fichier est uploadé. Elle prend en paramètres l'instance du modèle et le nom du fichier.
   - Elle utilise `datetime.now().strftime('%Y%m%d_%H%M%S')` pour générer une chaîne représentant la date et l'heure actuelles au format `YYYYMMDD_HHMMSS`.
   - Le chemin de destination pour le fichier est construit en concaténant ce timestamp avec le nom de fichier original.

> Mais personnellement, je vous déconseille d'utiliser le nom d'origine
> du fichier uploadé. Car, des fois, ce nom peut présenter quelques
> problème d'encodage de caractères, ce qui peut conduit à des bugs inexpliqués.

2. **Modèle `UploadedFile`** :
   - Le champ `title` permet de donner un titre au fichier.
   - Le champ `file_type` utilise des choix prédéfinis pour indiquer si le fichier est un document ou une image.
   - Le champ `file` utilise la fonction `upload_path` pour définir où et comment les fichiers sont stockés.
   - Le champ `uploaded_at` enregistre automatiquement la date et l'heure d'upload.

### Utilisation du modèle

Pour utiliser ce modèle, suivez ces étapes :

1. **Créer une migration** :
   Exécutez la commande suivante pour créer une migration :

   ```bash
   python manage.py makemigrations
   ```

2. **Appliquer la migration** :
   Appliquez la migration avec :

   ```bash
   python manage.py migrate
   ```

3. **Uploader des fichiers** :
   Vous pouvez maintenant créer des vues et des formulaires pour permettre aux utilisateurs d'uploader des documents et des images en utilisant ce modèle.


Avec ce modèle, chaque fichier uploadé aura un nom unique basé sur la date et l'heure de l'upload, ce qui facilite l'organisation et la gestion des fichiers dans votre application Django. Vous pouvez personnaliser davantage la fonction `upload_path` selon vos besoins spécifiques.

Références :

- [1] https://bdvade.hashnode.dev/structuring-file-uploads-in-django
- [2] https://forum.djangoproject.com/t/get-datetime-now-not-at-server-initialisation/4979
- [3] https://www.reddit.com/r/django/comments/l8iafj/looking_for_a_good_naming_convention_for/


## Filtrer les extensions
On peut placer un filtre sur le champ `FileField` dans votre modèle Django
pour limiter les types de fichiers autorisés à l'uploadage. Vous pouvez le faire
en utilisant des validateurs personnalisés ou en utilisant
le `FileExtensionValidator` intégré de Django. Voici comment procéder :

### Exemple de modèle avec validation de type de fichier

Voici un modèle qui utilise le `FileExtensionValidator` pour restreindre
les types de fichiers pouvant être uploadés :

```python
from django.db import models
from django.core.validators import FileExtensionValidator
from datetime import datetime

def upload_path(_instance, filename):
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"uploads/{current_time}_{filename}"

class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to=upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
```

### Explications

1. **FileExtensionValidator** :
   - Le `FileExtensionValidator` est utilisé pour spécifier les extensions
   - de fichiers autorisées. Dans cet exemple, seules les extensions
   `.pdf`, `.doc`, `.docx`, `.jpg`, `.jpeg`, et `.png` sont acceptées.
   - Si un utilisateur essaie d'uploader un fichier avec une extension
   non autorisée, une `ValidationError` sera levée.

2. **Fonction `upload_path`** :
   - Cette fonction génère un nom de fichier basé sur la date et l'heure
   actuelles pour éviter les conflits de noms.


### Validation supplémentaire

Il est important de noter que bien que le `FileExtensionValidator` soit utile,
il ne doit pas être la seule méthode de validation. Les utilisateurs peuvent
renommer des fichiers avec des extensions incorrectes. Pour une validation
plus robuste, vous pouvez également vérifier le type MIME du fichier
en utilisant une bibliothèque comme `python-magic`.

En intégrant un validateur directement sur le champ `FileField`,
vous pouvez contrôler efficacement les types de fichiers qui peuvent
être uploadés dans votre application Django. Cela améliore la sécurité
et garantit que seuls les fichiers appropriés sont stockés
dans votre base de données.

Références :

- [1] https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side
- [2] https://stackoverflow.com/questions/6460848/how-to-limit-file-types-on-file-uploads-for-modelforms-with-filefields
- [3] https://www.youtube.com/watch?v=UcUm82jWeKc
- [4] https://www.tutorialspoint.com/fileextensionvalidator-ndash-validate-file-extensions-in-django
