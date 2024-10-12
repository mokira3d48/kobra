# Formulaire Django

## Introduction
Les formulaires dans Django, en particulier ceux basés sur `forms.Form`,
sont utilisés pour gérer les entrées utilisateur, la validation des données
et le rendu des formulaires dans les templates. Voici un aperçu détaillé
de leur fonctionnement.

### Fonctionnalités de `forms.Form`

1. **Définition des champs** : Vous pouvez définir différents types de champs
pour capturer diverses entrées utilisateur, comme des chaînes de caractères,
des nombres, des dates, etc.

2. **Validation des données** : Django fournit un mécanisme intégré
pour valider les données saisies par l'utilisateur. Vous pouvez également
ajouter votre propre logique de validation.

3. **Rendu des formulaires** : Les formulaires peuvent être facilement
rendus dans les templates HTML, ce qui facilite leur intégration
dans l'interface utilisateur.

4. **Gestion des erreurs** : En cas d'erreur de validation,
Django gère automatiquement les messages d'erreur et les affiche
dans le formulaire.

### Exemple de code

#### 1. Définir un formulaire

Voici comment définir un formulaire personnalisé en utilisant `forms.Form` :

```python
# forms.py
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError(
                "Le message doit contenir au moins 10 caractères."
            )
        return message
```

### Explications des éléments

1. **Champs du formulaire** :
   - `name` : Un champ de type `CharField` qui accepte une chaîne
   de caractères avec une longueur maximale de 100 caractères.
   - `email` : Un champ de type `EmailField` qui valide que l'entrée 
   st une adresse e-mail valide.
   - `message` : Un champ de type `CharField`, mais avec un widget
   `Textarea` pour permettre une saisie multilignes.

2. **Validation personnalisée** :
   - La méthode `clean_message` est une méthode de validation personnalisée
   qui vérifie que le message contient au moins 10 caractères.
   Si ce n'est pas le cas, elle lève une `ValidationError`.

#### 2. Utiliser le formulaire dans une vue

Voici comment utiliser ce formulaire dans une vue :

```python
# views.py
from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Traitez les données du formulaire ici 
            # (par exemple, envoyez un e-mail)
            return render(request, 'success.html') 
            #: Rediriger vers une page de succès
    else:
        form = ContactForm()  # Créer un formulaire vide

    return render(request, 'contact.html', {'form': form})
```

### Explications des éléments

1. **Gestion des requêtes POST** :
   - Si la méthode de la requête est `POST`, le formulaire est instancié
   avec les données soumises (`request.POST`).
   - La méthode `is_valid()` est appelée pour valider les données.
   Si elles sont valides, vous pouvez traiter
   les données (comme envoyer un e-mail).

2. **Affichage du formulaire** :
   - Si la requête n'est pas `POST`, un nouveau formulaire vide est créé.
   - Le formulaire est passé au template pour être rendu.

#### 3. Rendu du formulaire dans le template

Voici comment rendre le formulaire dans un template HTML :

```html
<!-- contact.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}  <!-- Rendre le formulaire sous forme de paragraphes -->
    <button type="submit">Envoyer</button>
</form>

{% if form.errors %}
    <ul>
        {% for field in form %}
            {% for error in field.errors %}
                <li>{{ error }}</li>
            {% endfor %}
        {% endfor %}
        {% for error in form.non_field_errors %}
            <li>{{ error }}</li>
        {% endfor %}
    </ul>
{% endif %}
```

Les formulaires Django basés sur `forms.Form` offrent une manière puissante
et flexible de gérer les entrées utilisateur et la validation.
Ils permettent également une intégration facile avec l'interface utilisateur
grâce à leur capacité à être rendus dans des templates HTML.
Pour plus d'informations détaillées,
consultez la [documentation officielle de Django sur les formulaires](https://docs.djangoproject.com/en/stable/topics/forms/).


## Formulaire conditionnel
Pour ajouter des champs de formulaire conditionnels dans Django,
vous pouvez utiliser plusieurs approches. Voici un guide détaillé
sur la manière d'implémenter des champs conditionnels dans vos formulaires
Django.

### Méthode 1 : Utiliser JavaScript pour le rendu dynamique

La méthode la plus courante consiste à utiliser JavaScript pour afficher
ou masquer des champs en fonction des réponses de l'utilisateur.
Voici comment procéder :

#### Étapes

1. **Créer le formulaire** : Définissez votre formulaire avec tous les champs
nécessaires, y compris ceux qui seront affichés conditionnellement.

2. **Rendre le formulaire dans le template** : Utilisez des attributs `id`
et `class` pour cibler les éléments avec JavaScript.

3. **Ajouter du JavaScript** : Écrivez un script pour gérer l'affichage
des champs en fonction des valeurs saisies.

#### Exemple de code

##### 1. Définir le formulaire

```python
# forms.py
from django import forms

class MyForm(forms.Form):
    has_vehicle = forms.BooleanField(required=False)
    vehicle_description = forms.CharField(required=False)
```

##### 2. Rendre le formulaire dans le template

```html
<!-- template.html -->
<form method="post">
    {% csrf_token %}
    <label for="id_has_vehicle">Possédez-vous un véhicule ?</label>
    {{ form.has_vehicle }}

    <div id="vehicle-description" style="display: none;">
        <label for="id_vehicle_description">Description du véhicule :</label>
        {{ form.vehicle_description }}
    </div>

    <button type="submit">Soumettre</button>
</form>

<script>
document.getElementById('id_has_vehicle').addEventListener('change', function() {
    var vehicleDescription = document.getElementById('vehicle-description');
    if (this.checked) {
        vehicleDescription.style.display = 'block';
    } else {
        vehicleDescription.style.display = 'none';
    }
});
</script>
```

### Méthode 2 : Validation conditionnelle dans le backend

Vous pouvez également gérer la logique conditionnelle côté serveur
en utilisant la méthode `clean()` de votre formulaire.

#### Exemple de code
Dans cet exemple, on définit la logique de validation.

```python
# forms.py
from django import forms

class MyForm(forms.Form):
    has_vehicle = forms.BooleanField(required=False)
    vehicle_description = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        has_vehicle = cleaned_data.get("has_vehicle")
        vehicle_description = cleaned_data.get("vehicle_description")

        if has_vehicle and not vehicle_description:
            self.add_error('vehicle_description',
                           "Veuillez fournir une description du véhicule.")
```

En utilisant ces méthodes, vous pouvez facilement ajouter des champs
de formulaire conditionnels dans vos applications Django. La première méthode
utilise JavaScript pour un rendu dynamique côté client, tandis que la seconde
gère la logique conditionnelle côté serveur lors de la validation
du formulaire. Choisissez l'approche qui convient le mieux à vos besoins
et à votre architecture d'application.

### Références

- [1] https://doc-publik.entrouvert.com/admin-fonctionnel/fabrique-formulaires/creer-un-formulaire-conditionnel/
- [2] https://docs.djangoproject.com/fr/5.1/ref/forms/fields/
- [3] https://docs.djangoproject.com/fr/5.1/ref/contrib/admin/
- [4] https://developer.mozilla.org/fr/docs/Learn/Server-side/Django/Forms
- [5] https://djangospirit.readthedocs.io/en/latest/topics/forms/
- [6] https://docs.djangoproject.com/fr/5.1/topics/forms/
- [7] https://openclassrooms.com/forum/sujet/creer-formulaire-avec-ajout-de-champs
- [8] https://docs.djangoproject.com/en/5.1/ref/contrib/admin/


## Formulaire personnalisé

Pour créer des formulaires personnalisés dans Django, vous pouvez utiliser
à la fois `forms.Form` et `forms.ModelForm`. Voici un aperçu détaillé
de leur fonctionnement et de la manière dont vous pouvez les personnaliser.

### 1. Définir un formulaire avec `forms.Form`

Cette méthode vous permet de créer un formulaire sans lier directement
les champs à un modèle.
Exemple de formulaire :

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError(
            "Le message doit contenir au moins 10 caractères."
        )
        return message
```

### 2. Utiliser `forms.ModelForm`

Si vous avez un modèle Django et que vous souhaitez créer un formulaire basé
sur ce modèle, utilisez `ModelForm`. Cela permet de générer automatiquement
les champs du formulaire en fonction des champs du modèle.
Exemple de `ModelForm` :

```python
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
```

### 3. Personnalisation des formulaires

#### a. Widgets

Vous pouvez personnaliser le rendu des champs en utilisant des widgets.
Par exemple, pour utiliser un champ de texte plus grand :

```python
class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField(widget=forms.Textarea)
```

#### b. Attributs HTML

Vous pouvez ajouter des attributs HTML supplémentaires aux champs :

```python
class CommentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'special', 'placeholder': 'Votre nom'}
    ))
```

#### c. Validation personnalisée

Vous pouvez ajouter votre propre logique de validation dans la méthode
`clean()` ou pour des champs spécifiques :

```python
def clean_email(self):
    email = self.cleaned_data.get('email')
    if not email.endswith('@example.com'):
        raise forms.ValidationError("L'email doit être un @example.com.")
    return email
```

### 4. Rendu du formulaire dans le template

Pour afficher le formulaire dans un template, vous pouvez utiliser :

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}  <!-- Rendu sous forme de paragraphes -->
    <button type="submit">Envoyer</button>
</form>
```

Les formulaires personnalisés dans Django offrent une grande flexibilité
pour gérer les entrées utilisateur et valider les données. Que vous utilisiez
`forms.Form` ou `forms.ModelForm`, vous pouvez facilement personnaliser
le rendu, ajouter des validations et gérer les erreurs.
Pour plus d'informations détaillées,
consultez la [documentation officielle de Django sur les formulaires](https://docs.djangoproject.com/en/stable/topics/forms/).

### Références
- [1] https://docs.djangoproject.com/fr/5.1/ref/forms/widgets/
- [2] https://docs.djangoproject.com/fr/5.1/ref/forms/fields/
- [3] https://www.univ-orleans.fr/iut-orleans/informatique/intra/tuto/django/django-forms.html
- [4] https://tutorial.djangogirls.org/fr/django_forms/
- [5] https://placepython.fr/webinaire/comment-personnaliser-le-rendu-de-vos-formulaires-avec-django-crispy-forms/
- [6] https://docs.djangoproject.com/fr/5.1/ref/contrib/admin/
- [7] https://docs.djangoproject.com/fr/5.1/topics/forms/
- [8] https://djangospirit.readthedocs.io/en/latest/topics/forms/

