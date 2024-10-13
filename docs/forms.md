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

- `CharField` : pour du texte;
- `IntegerField` : pour des nombres entiers;
- `DateField` : pour des dates;
- `EmailField` : pour des adresses e-mail;
- `FileField` : pour l'upload de fichiers;
- `ChoiceField` : pour des choix prédéfinis;

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
document.getElementById('id_has_vehicle')
        .addEventListener('change', function() {
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


## Type de champs de base
Très bien, concentrons-nous sur la création et la personnalisation des champs
de formulaire en Django. C'est un aspect fondamental pour construire
des formulaires efficaces et adaptés à vos besoins spécifiques.

### 1. Types de champs de base :

Django fournit de nombreux types de champs prédéfinis.
Voici les plus courants :

- `CharField` : Pour du texte court;
- `TextField` : Pour du texte long;
- `IntegerField` : Pour des nombres entiers;
- `FloatField` : Pour des nombres décimaux;
- `BooleanField` : Pour des valeurs vrai/faux;
- `DateField` : Pour des dates;
- `DateTimeField` : Pour des dates avec heure;
- `EmailField` : Pour des adresses e-mail;
- `FileField` : Pour l'upload de fichiers;
- `ImageField` : Pour l'upload d'images.

### 2. Création d'un champ personnalisé :

Vous pouvez créer vos propres champs en héritant de `forms.Field` :

```python
from django import forms

class AgeField(forms.Field):
    def to_python(self, value):
        try:
            return int(value)
        except ValueError:
            raise forms.ValidationError("Veuillez entrer un nombre entier.")

    def validate(self, value):
        if value < 0 or value > 120:
            raise forms.ValidationError(
                "L'âge doit être compris entre 0 et 120."
            )
```

### 3. Personnalisation des champs existants :

Vous pouvez personnaliser les champs existants en ajoutant des arguments :

```python
class MonFormulaire(forms.Form):
    nom = forms.CharField(
        max_length=100,
        required=True,
        label="Votre nom",
        help_text="Entrez votre nom complet",
        initial="M./Mme",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
```

### 4. Widgets :

Les widgets déterminent le rendu HTML du champ. Vous pouvez les personnaliser :

```python
class MonFormulaire(forms.Form):
    choix = forms.ChoiceField(
        choices=[('1', 'Option 1'), ('2', 'Option 2')],
        widget=forms.RadioSelect
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
```

### 5. Validation au niveau du champ :

Ajoutez des validateurs personnalisés à vos champs :

```python
from django.core.validators import RegexValidator

class MonFormulaire(forms.Form):
    code_postal = forms.CharField(
        validators=[
            RegexValidator(r'^\d{5}$', 'Entrez un code postal valide.')
        ]
    )
```

### 6. Champs dynamiques :

Vous pouvez ajouter ou modifier des champs dynamiquement :

```python
class MonFormulaireDynamique(forms.Form):
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields', None)
        super(MonFormulaireDynamique, self).__init__(*args, **kwargs)
        if extra_fields:
            for field_name, field_type in extra_fields.items():
                self.fields[field_name] = field_type()
```

### 7. Champs composés :

Créez des champs composés pour des données complexes :

```python
class CoordonneeField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.FloatField(),
            forms.FloatField(),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return tuple(data_list)
        return None
```

Ces techniques vous permettent de créer des formulaires Django hautement
personnalisés. Vous pouvez ajuster chaque champ pour qu'il corresponde
exactement à vos besoins en termes de validation, de présentation
et de fonctionnalité.


### 8. Internationalisation des champs de formulaire

L'internationalisation (i18n) est cruciale pour créer des applications
multilingues. Django offre d'excellents outils pour internationaliser
vos formulaires.

a) Traduction des chaînes de caractères :
Utilisez la fonction `gettext_lazy` (généralement importée comme `_`)
pour marquer les chaînes à traduire :

```python
from django import forms
from django.utils.translation import gettext_lazy as _

class MonFormulaire(forms.Form):
    nom = forms.CharField(label=_("Nom"),
                          help_text=_("Entrez votre nom complet"))
    email = forms.EmailField(label=_("Adresse e-mail"))
```

b) Traduction des choix dans les champs de sélection :
Pour les `ChoiceField`, vous pouvez utiliser des tuples
avec des chaînes traduisibles :

```python
CHOIX_PAYS = [
    ('FR', _('France')),
    ('DE', _('Allemagne')),
    ('ES', _('Espagne')),
]

class FormulaireInternational(forms.Form):
    pays = forms.ChoiceField(choices=CHOIX_PAYS, label=_("Pays"))
```

c) Gestion des formats de date :
Django adapte automatiquement les formats de date selon la locale :

```python
class FormulaireDate(forms.Form):
    date_naissance = forms.DateField(
        label=_("Date de naissance"),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
```

d) Validation des messages d'erreur :
Assurez-vous que les messages d'erreur sont également traduisibles :

```python
from django.core.exceptions import ValidationError

def valider_age(value):
    if value < 18:
        raise ValidationError(_("Vous devez avoir au moins 18 ans."))

class FormulaireAge(forms.Form):
    age = forms.IntegerField(validators=[valider_age])
```

### 9. Création de champs pour des types de données spécifiques

Maintenant, abordons la création de champs pour des types de données
spécifiques, comme les coordonnées géographiques et les intervalles de temps.

a) Champ pour les coordonnées géographiques :

```python
from django import forms
from django.core.exceptions import ValidationError

class CoordonneesGeographiquesField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.FloatField(min_value=-90, max_value=90),
            forms.FloatField(min_value=-180, max_value=180),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return tuple(data_list)
        return None

    def clean(self, value):
        super().clean(value)
        if value:
            lat, lon = value
            if lat == 0 and lon == 0:
                raise ValidationError(_("Les coordonnées 0,0 sont invalides."))
        return value

class FormulaireGeographique(forms.Form):
    coordonnees = CoordonneesGeographiquesField(
        label=_("Coordonnées (latitude, longitude)"),
        help_text=_("Entrez la latitude "
                    "et la longitude séparées par une virgule")
    )
```

b) Champ pour les intervalles de temps :

```python
from datetime import timedelta

class IntervalleTempsField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(min_value=0),
            forms.ChoiceField(choices=[
                ('minutes', _('Minutes')),
                ('heures', _('Heures')),
                ('jours', _('Jours')),
            ])
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            valeur, unite = data_list
            if unite == 'minutes':
                return timedelta(minutes=valeur)
            elif unite == 'heures':
                return timedelta(hours=valeur)
            elif unite == 'jours':
                return timedelta(days=valeur)
        return None

class FormulaireDuree(forms.Form):
    duree = IntervalleTempsField(
        label=_("Durée"),
        help_text=_("Entrez une durée et choisissez l'unité")
    )
```

Ces exemples montrent comment créer des champs personnalisés pour gérer
des types de données spécifiques tout en intégrant l'internationalisation.
Ils combinent validation, formatage et traduction pour offrir une expérience
utilisateur cohérente dans différentes langues.


## Techniques de validation avancées

### 1. Validation au niveau du champ

a) Méthode `clean_<fieldname>()` :
Cette méthode permet une validation spécifique pour un champ donné.

```python
class MonFormulaire(forms.Form):
    username = forms.CharField(max_length=100)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username
```

b) Validateurs personnalisés :
Vous pouvez créer des fonctions de validation réutilisables.

```python
from django.core.exceptions import ValidationError

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s n'est pas un nombre pair',
                              params={'value': value})

class MonFormulaire(forms.Form):
    even_number = forms.IntegerField(validators=[validate_even])
```

### 2. Validation au niveau du formulaire

a) Méthode `clean()` :
Utilisée pour la validation impliquant plusieurs champs.

```python
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                "Les nouveaux mots de passe ne correspondent pas."
            )
        return cleaned_data
```

### 3. Validation asynchrone

Pour des validations nécessitant des opérations asynchrones
(comme des requêtes API):

```python
import asyncio
from django import forms

class AsyncForm(forms.Form):
    email = forms.EmailField()

    async def async_clean_email(self):
        email = self.cleaned_data['email']
        # Simulation d'une vérification asynchrone
        await asyncio.sleep(1)
        if "example.com" in email:
            raise forms.ValidationError(
                "Les adresses example.com ne sont pas autorisées."
            )
        return email

    def clean_email(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.async_clean_email())
```

### 4. Validation conditionnelle

Validation basée sur des conditions spécifiques :

```python
class CommandeForm(forms.Form):
    produit = forms.CharField()
    quantite = forms.IntegerField(min_value=1)
    code_promo = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        produit = cleaned_data.get('produit')
        code_promo = cleaned_data.get('code_promo')

        if produit == 'premium' and not code_promo:
            raise forms.ValidationError("Un code promo est requis "
                                        "pour les produits premium.")

        return cleaned_data
```

### 5. Validation personnalisée avec contexte

Utilisation de validateurs personnalisés avec accès au contexte
du formulaire :

```python
from django.core.exceptions import ValidationError

def validate_unique_together(value, form_instance):
    if form_instance.instance.pk is None:  # Nouveau formulaire
        if MyModel.objects.filter(field1=form_instance.cleaned_data['field1'], 
                                  field2=value).exists():
            raise ValidationError("Cette combinaison existe déjà.")

class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['field1', 'field2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['field2'].validators.append(
            lambda value: validate_unique_together(value, self)
        )
```

### 6. Validation dépendante du modèle

Pour les ModelForms, vous pouvez surcharger la méthode `clean()`
pour inclure une logique de validation spécifique au modèle :

```python
from django.core.exceptions import ValidationError

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'birth_date']

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        birth_date = cleaned_data.get('birth_date')

        if user and birth_date:
            if user.date_joined.date() < birth_date:
                raise ValidationError("La date de naissance "
                                      "ne peut pas être postérieure "
                                      "à la date d'inscription.")

        return cleaned_data
```

Ces techniques de validation avancées vous permettent de gérer des scénarios
complexes et d'assurer l'intégrité des données dans vos formulaires Django.
Elles offrent une grande flexibilité pour implémenter des règles de validation
personnalisées et spécifiques à votre application.

## Formulaire dynamique ou Ajax
Les formulaires dynamiques ou AJAX sont une excellente façon d'améliorer
l'expérience utilisateur en rendant vos formulaires plus interactifs
et réactifs. Voici une explication détaillée de leur fonctionnement :

### 1. Formulaires Dynamiques

Les formulaires dynamiques sont des formulaires dont le contenu
ou le comportement peut changer en fonction des interactions de l'utilisateur,
sans nécessiter un rechargement complet de la page.

a) Côté serveur (Django) :

```python
from django import forms

class DynamicForm(forms.Form):
    TYPE_CHOICES = [
        ('individuel', 'Individuel'),
        ('entreprise', 'Entreprise'),
    ]

    type_client = forms.ChoiceField(choices=TYPE_CHOICES)
    nom = forms.CharField(max_length=100)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'data' in kwargs \
            and kwargs['data'].get('type_client') == 'entreprise':
            self.fields['siret'] = forms.CharField(max_length=14)

class DynamicFormView(View):
    def get(self, request):
        form = DynamicForm()
        return render(request, 'dynamic_form.html', {'form': form})

    def post(self, request):
        form = DynamicForm(request.POST)
        if form.is_valid():
            # Traitement du formulaire
            return redirect('success')
        return render(request, 'dynamic_form.html', {'form': form})
```

b) Côté client (JavaScript) :

```javascript
document.addEventListener('DOMContentLoaded', function() {
    var typeClient = document.getElementById('id_type_client');
    var formContainer = document.getElementById('form-container');

    typeClient.addEventListener('change', function() {
        if (this.value === 'entreprise') {
            var siretField = document.createElement('div');
            siretField.innerHTML = (
                '<label for="id_siret">SIRET:</label>' +
                '<input type="text" name="siret" maxlength="14" id="id_siret" required>');
            formContainer.appendChild(siretField);
        } else {
            var existingSiretField = document.getElementById('id_siret');
            if (existingSiretField) {
                existingSiretField.parentNode.remove();
            }
        }
    });
});
```

### 2. Formulaires AJAX

Les formulaires AJAX permettent de soumettre des données au serveur
et de recevoir une réponse sans recharger la page entière.

a) Côté serveur (Django) :

```python
from django.http import JsonResponse

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

class AjaxFormView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'ajax_form.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'success': True,
                'redirect': reverse('profile')
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
```

b) Côté client (JavaScript avec jQuery pour simplifier) :

```javascript
$(document).ready(function() {
    $('#id_username').change(function() {
        var username = $(this).val();
        $.ajax({
            url: '/validate_username/',
            data: {
                'username': username
            },
            dataType: 'json',
            success: function(data) {
                if (data.is_taken) {
                    $('#username-error').text(
                        'Ce nom d\'utilisateur est déjà pris.'
                    );
                } else {
                    $('#username-error').text('');
                }
            }
        });
    });

    $('#registration-form').submit(function(e) {
        e.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/register/',
            data: formData,
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    window.location.href = response.redirect;
                } else {
                    // Afficher les erreurs
                    $.each(response.errors, function(key, value) {
                        $('#' + key + '-error').text(value);
                    });
                }
            }
        });
    });
});
```

### 3. Bonnes pratiques

- Utilisez Django REST framework pour des API plus robustes
si votre application le nécessite.
- Pensez à la sécurité : utilisez des jetons CSRF pour les requêtes POST AJAX.
- Gérez les erreurs côté client et serveur.
- Utilisez des bibliothèques comme htmx ou Alpine.js pour simplifier
les interactions AJAX.

### 4. Exemple avec htmx

htmx permet de créer des interfaces dynamiques avec très peu de JavaScript :

```html
{% load static %}
<script src="{% static 'htmx.min.js' %}" defer></script>

<form hx-post="/register/" hx-swap="outerHTML">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">S'inscrire</button>
</form>
```

Dans ce cas, Django peut renvoyer du HTML partiel en réponse
à la requête AJAX, simplifiant grandement la logique côté client.

Les formulaires dynamiques et AJAX offrent une grande flexibilité
pour créer des interfaces utilisateur réactives et améliorent
significativement l'expérience utilisateur en réduisant les temps
de chargement et en permettant des interactions plus fluides.


## Bonne pratiques
La sécurité des formulaires est cruciale pour protéger
votre application et les données de vos utilisateurs. Voici les bonnes
pratiques en matière de sécurité pour les formulaires Django :

1. Protection contre les attaques CSRF (Cross-Site Request Forgery)

Django intègre une protection CSRF par défaut. Assurez-vous de l'utiliser
correctement :

- Incluez le jeton CSRF dans vos formulaires :

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Envoyer</button>
</form>
```

- Pour les requêtes AJAX, incluez le jeton CSRF dans les en-têtes :

```javascript
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

fetch('/url/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
})
```

2. Validation des données côté serveur

Ne faites jamais confiance aux données entrées par l'utilisateur.
Validez toujours côté serveur :

```python
from forms import ValidationError


class MonFormulaire(forms.Form):
    email = forms.EmailField()
    age = forms.IntegerField(min_value=0, max_value=120)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.endswith('exemple.com'):
            raise ValidationError("Cette adresse email n'est pas autorisée.")
        return email
```

3. Protection contre l'injection SQL

Django's ORM protège contre l'injection SQL par défaut. Évitez les requêtes
SQL brutes avec des paramètres non échappés :

```python
# Mauvais (vulnérable à l'injection SQL)
User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")

# Bon
User.objects.raw("SELECT * FROM auth_user WHERE username = %s", [username])

# Meilleur (utilisation de l'ORM)
User.objects.filter(username=username)
```

4. Limitation du taux de soumission

Implémentez une limitation du taux pour prévenir les attaques par force brute :

```python
from django.core.cache import cache
from django.core.exceptions import ValidationError


class RateLimitedForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        ip = self.request.META.get('REMOTE_ADDR')
        key = f'form_submit_{ip}'
        if cache.get(key, 0) >= 5:
            raise ValidationError("Trop de tentatives. "
                                  "Veuillez réessayer plus tard.")
        cache.set(key, cache.get(key, 0) + 1, 300)  # 5 minutes
        return cleaned_data
```

5. Sécurisation des uploads de fichiers

Si votre formulaire accepte des fichiers :

```python
class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            if file.size > 5 * 1024 * 1024:  # 5 MB
                raise forms.ValidationError("Le fichier est trop volumineux.")
            fn_lower = file.name.lower()
            if not fn_lower.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError("Type de fichier non autorisé.")
        return file
```

6. Protection contre le clickjacking

Utilisez les en-têtes X-Frame-Options :

```python
MIDDLEWARE = [
    ...
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ...
]

X_FRAME_OPTIONS = 'DENY'
```

7. Sécurité des sessions

Configurez correctement les paramètres de session :

```python
SESSION_COOKIE_SECURE = True  # Utilise HTTPS
SESSION_COOKIE_HTTPONLY = True  # Empêche l'accès JS aux cookies
```

8. Sanitisation des entrées HTML

Si vous autorisez le HTML dans certains champs, utilisez une bibliothèque
comme `bleach` pour nettoyer les entrées :

```python
import bleach

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

    def clean_content(self):
        content = self.cleaned_data['content']
        return bleach.clean(content, tags=['p', 'b', 'i', 'u', 'a'],
                            attributes={'a': ['href']})
```

9. Utilisation de captcha pour les formulaires publics

Intégrez reCAPTCHA ou un système similaire pour les formulaires accessibles
publiquement :

```python
from captcha.fields import ReCaptchaField

class PublicForm(forms.Form):
    # ... autres champs
    captcha = ReCaptchaField()
```

10. Principe du moindre privilège

Assurez-vous que vos vues de traitement de formulaires n'effectuent
que les actions nécessaires et rien de plus.

11. Journalisation des actions sensibles

Enregistrez les actions sensibles pour faciliter l'audit
et la détection d'activités suspectes :

```python
import logging

logger = logging.getLogger(__name__)

def process_sensitive_form(request):
    if form.is_valid():
        # Traitement du formulaire
        logger.info("Action sensible effectuée "
                    f"par l'utilisateur {request.user.username}")
```

12. Utilisation de HTTPS

Assurez-vous que tous les formulaires, en particulier ceux traitant
des données sensibles, sont soumis via HTTPS.

En suivant ces bonnes pratiques, vous pouvez considérablement renforcer
la sécurité de vos formulaires Django et protéger votre application
contre de nombreuses menaces courantes. N'oubliez pas que la sécurité
est un processus continu, et il est important de rester à jour
avec les dernières recommandations et correctifs de sécurité.

