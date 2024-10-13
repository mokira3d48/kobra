# CKEditor

## Installation de CKEditor
Pour installer et configurer CKEditor dans l'administration de Django,
suivez les étapes ci-dessous :

### Étapes d'installation et de configuration

1. Installer django-ckeditor

Exécutez la commande suivante pour installer le package `django-ckeditor` :

```bash
pip install django-ckeditor
```

2. Ajouter à `INSTALLED_APPS`

Ajoutez `ckeditor` et `ckeditor_uploader` à la liste des applications
installées dans votre fichier `settings.py` :

```python
# settings.py

INSTALLED_APPS = [
    # autres applications
    'ckeditor',
    'ckeditor_uploader',
]
```

3. Configurer les URL

Ajoutez les URL de CKEditor dans votre fichier `urls.py` principal :

```python
# urls.py

from django.urls import path, include

urlpatterns = [
    # autres routes
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
```

4. Configurer les paramètres de CKEditor

Ajoutez les paramètres de configuration pour CKEditor dans votre fichier
`settings.py`. Voici un exemple de configuration :

```python
# settings.py

CKEDITOR_UPLOAD_PATH = "uploads/"
#: Dossier où les fichiers uploadés seront stockés

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule']},
            {'name': 'styles', 'items': ['Format', 'FontSize']},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline']},
        ],
        'height': 300,
        'width': 800,
    },
}
```

5. Utiliser CKEditor dans un modèle

Pour utiliser CKEditor dans un modèle, importez le champ `RichTextField`
et utilisez-le dans votre modèle :

```python
# models.py

from django.db import models
from ckeditor.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(config_name='default')
    #: Utiliser CKEditor pour le champ content

    def __str__(self):
        return self.title
```

6. Migrer la base de données

Si vous avez ajouté un nouveau modèle, n'oubliez pas de créer et d'appliquer
les migrations :

```bash
python manage.py makemigrations
python manage.py migrate
```

Après avoir suivi ces étapes, CKEditor devrait être correctement installé
et configuré dans l'administration de Django. Vous pourrez maintenant utiliser
l'éditeur WYSIWYG pour vos champs de texte enrichi dans l'interface
d'administration. Pour plus d'informations,
consultez la [documentation officielle de django-ckeditor](https://github.com/django-ckeditor/django-ckeditor).

## Utilisation avancée
Dans le fichier `settings.py`, on peut écrire la configuration suivante :

```python
CKEDITOR_CONFIGS = {
    'advanced': {
        'skin': 'moono-lisa',
        'toolbar_Advanced': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike',
             'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'],
            ['Source'],
        ],
        'toolbar': 'Advanced',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

```

1. Utilisation dans les modèles

Voici comment utiliser CKEditor dans vos modèles :

```python
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(config_name='advanced')
    content_with_images = RichTextUploadingField(config_name='advanced')
```

2. Personnalisation de l'admin

Pour une utilisation vraiment avancée, vous pouvez personnaliser l'apparence et le comportement de CKEditor dans l'admin Django :



```python
from django.contrib import admin
from django.db import models
from .models import Post
from ckeditor.widgets import CKEditorWidget

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='advanced')},
    }
    
    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js',
            '/static/js/custom_ckeditor.js',
        )
        css = {
            'all': ('/static/css/custom_ckeditor.css',)
        }

admin.site.register(Post, PostAdmin)

```

Dans cet exemple, nous ajoutons des fichiers JS et CSS personnalisés pour modifier le comportement de CKEditor.

3. Intégration avec Django-filebrowser

Pour une gestion avancée des fichiers, vous pouvez intégrer CKEditor avec django-filebrowser :

```python
CKEDITOR_CONFIGS = {
    'advanced': {
        ...
        'filebrowserBrowseUrl': '/admin/filebrowser/browse/?pop=3',
        'filebrowserImageBrowseUrl': '/admin/filebrowser/browse/?pop=3&type=Image',
        ...
    }
}
```

4. Validation côté serveur

Pour une sécurité accrue, vous pouvez ajouter une validation côté serveur du contenu HTML :

```python
from django.core.exceptions import ValidationError
from bleach import clean

def validate_content(value):
    cleaned_content = clean(value, strip=True)
    if len(cleaned_content) < 10:
        raise ValidationError("Le contenu est trop court.")

class Post(models.Model):
    content = RichTextField(config_name='advanced', validators=[validate_content])
```

5. Champs CKEditor personnalisés

Vous pouvez créer des champs CKEditor personnalisés pour des besoins spécifiques :



```python
from ckeditor.fields import RichTextField
from django.db import models

class LimitedRichTextField(RichTextField):
    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.pop('max_length', None)
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        data = super().clean(value, model_instance)
        if self.max_length and len(data) > self.max_length:
            raise ValidationError(f'Le contenu dépasse la longueur maximale de {self.max_length} caractères.')
        return data

class Post(models.Model):
    content = LimitedRichTextField(max_length=1000, config_name='advanced')

```

Ce champ personnalisé limite la longueur du contenu HTML.

6. Prévisualisation en temps réel

Vous pouvez ajouter une prévisualisation en temps réel du contenu édité dans l'admin :

1. Ajoutez une vue pour la prévisualisation :

```python
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def preview_content(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        return HttpResponse(content)
    return HttpResponse('Méthode non autorisée', status=405)
```

2. Ajoutez l'URL dans urls.py :

```python
urlpatterns = [
    ...
    path('preview/', preview_content, name='preview_content'),
    ...
]
```

3. Ajoutez du JavaScript personnalisé pour la prévisualisation en temps réel.

Ces techniques avancées vous permettent de tirer le meilleur parti de CKEditor dans l'admin Django, offrant une expérience d'édition de contenu riche et personnalisée.

Voulez-vous que je développe l'un de ces aspects en particulier ou que j'aborde un autre sujet lié à CKEditor dans Django ?

## Uploadage et positionnement d'images
Excellent choix. L'upload d'images et leur positionnement dans CKEditor est un sujet important pour créer une expérience d'édition riche. Je vais vous expliquer en détail comment configurer et utiliser cette fonctionnalité.

1. Configuration de l'upload d'images

Tout d'abord, assurez-vous d'avoir installé django-ckeditor
avec le support d'upload :

```
pip install django-ckeditor[pillow]
```

Ensuite, configurez les paramètres dans votre fichier settings.py :



```python
import os

INSTALLED_APPS = [
    ...
    'ckeditor',
    'ckeditor_uploader',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage',
            'image2',
        ]),
        'removePlugins': ','.join([
            'image',
        ]),
        'image2_alignClasses': ['image-align-left', 'image-align-center',
                                'image-align-right'],
        'image2_disableResizer': True,
    }
}

```

2. Configuration des URLs

Dans votre fichier urls.py principal :

```python
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    ...
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

3. Utilisation dans les modèles

Utilisez RichTextUploadingField pour les champs qui doivent supporter l'upload d'images :

```python
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    content = RichTextUploadingField()
```

4. Personnalisation de l'upload et du positionnement des images

Pour un contrôle plus fin sur l'upload et le positionnement des images, vous pouvez personnaliser la configuration de CKEditor :

```python
CKEDITOR_CONFIGS = {
    'advanced_image': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Image', 'Table'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'height': 400,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage',
            'image2',
            'dialogui',
            'dialog',
        ]),
        'removePlugins': ','.join([
            'image',
        ]),
        'image2_alignClasses': ['image-align-left', 'image-align-center', 'image-align-right'],
        'image2_disableResizer': False,
        'image2_captionedClass': 'image-captioned',
        'image2_prefillDimensions': False,
    }
}
```

Dans cette configuration :
- Nous utilisons le plugin 'image2' qui offre plus de flexibilité pour le positionnement des images.
- `image2_alignClasses` définit les classes CSS pour l'alignement des images.
- `image2_disableResizer` permet de redimensionner les images dans l'éditeur.
- `image2_captionedClass` ajoute une classe pour les images avec légende.

5. Styles CSS personnalisés

Pour que le positionnement des images fonctionne correctement, vous devez ajouter des styles CSS correspondants :
```css
<antArtifact identifier="ckeditor-image-positioning-css" type="application/vnd.ant.code" language="css" title="Styles CSS pour le positionnement des images dans CKEditor">
.image-align-left {
    float: left;
    margin-right: 10px;
}

.image-align-center {
    display: block;
    margin-left: auto;
    margin-right: auto;
}

.image-align-right {
    float: right;
    margin-left: 10px;
}

.image-captioned {
    border: 1px solid #ccc;
    padding: 5px;
}

.image-captioned figcaption {
    background-color: #f7f7f7;
    padding: 5px;
    text-align: center;
}
```


6. Gestion des uploads côté serveur

Pour un contrôle plus fin sur les uploads d'images, vous pouvez personnaliser le processus d'upload :

```python
from django.conf import settings
import os
from datetime import datetime

def custom_upload_to(instance, filename):
    now = datetime.now()
    path = f"uploads/{now.year}/{now.month:02d}/{now.day:02d}/"
    ext = filename.split('.')[-1]
    filename = f"{now.timestamp()}.{ext}"
    return os.path.join(path, filename)

class Post(models.Model):
    image = models.ImageField(upload_to=custom_upload_to)
    content = RichTextUploadingField(config_name='advanced_image')
```

7. Sécurité

N'oubliez pas d'implémenter des mesures de sécurité pour les uploads d'images :

- Limitez les types de fichiers autorisés
- Vérifiez la taille des fichiers
- Scannez les fichiers pour détecter les malwares

Exemple de validation :

```python
from django.core.exceptions import ValidationError

def validate_image(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(
            f"La taille maximale de l'image est de {limit_mb}MB"
        )

class Post(models.Model):
    image = models.ImageField(upload_to=custom_upload_to, validators=[validate_image])
```

Ces configurations et techniques vous permettront d'avoir un contrôle fin sur l'upload et le positionnement des images dans CKEditor, offrant ainsi une expérience d'édition riche et flexible pour vos utilisateurs.



