# Django ModelAdmin

## Introduction

La classe `admin.ModelAdmin` dans Django est utilisée pour personnaliser
l'affichage et le comportement des modèles dans l'interface d'administration.
Voici un aperçu de son fonctionnement et de ses principales caractéristiques.

### Fonctionnalités de `admin.ModelAdmin`

1. Enregistrement des Modèles :
- Pour utiliser `ModelAdmin`, vous devez d'abord définir une sous-classe
de `ModelAdmin` pour chaque modèle que vous souhaitez personnaliser.
- Ensuite, vous enregistrez cette classe avec le modèle correspondant
à l'aide de `admin.site.register()` ou du décorateur `@admin.register()`.

```python
from django.contrib import admin
from .models import Author, Book

class AuthorAdmin(admin.ModelAdmin):
   list_display = ('last_name', 'first_name', 'date_of_birth')

admin.site.register(Author, AuthorAdmin)
```

Voici un autre exemple d'utilisation. Supposons que vous ayez un modèle
`Book` :

```python
# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title
```

Si vous souhaitez afficher des informations dérivées ou formatées,
vous pouvez définir des méthodes dans votre classe `ModelAdmin`.
Par exemple, si vous voulez afficher le prix formaté :

```python
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'formatted_price')

    def formatted_price(self, obj):
        return f"${obj.price:.2f}"  # Formatage du prix avec un symbole dollar
    formatted_price.short_description = "Price"  # Titre de la colonne

admin.site.register(Book, BookAdmin)
```

- **list_display** : Cette propriété prend une liste de noms de champs
du modèle ou de méthodes définies dans la classe. Chaque élément
de cette liste correspond à une colonne dans la vue de liste.
  
- **Méthodes personnalisées** : Les méthodes ajoutées à `list_display`
doivent prendre un paramètre (généralement nommé `obj`) qui représente
l'instance du modèle en cours d'affichage. Vous pouvez également définir
un attribut `short_description` pour personnaliser le titre de la colonne.

2. Personnalisation de l'Interface :
- **`list_display`** : Permet de spécifier les champs à afficher
dans la liste des objets. Par exemple, vous pouvez afficher le prénom
et le nom de famille d'un auteur.

```python
class AuthorAdmin(admin.ModelAdmin):
   list_display = ('last_name', 'first_name', 'date_of_birth')
```

- **`search_fields`** : Permet d'ajouter une barre de recherche pour filtrer
les résultats par les champs spécifiés.

```python
class AuthorAdmin(admin.ModelAdmin):
   search_fields = ('last_name', 'first_name')
```

- **`list_filter`** : Ajoute des filtres latéraux pour affiner les résultats
affichés.

```python
class BookAdmin(admin.ModelAdmin):
   list_filter = ('genre',)
```

3. Formulaires Personnalisés :
Vous pouvez utiliser un formulaire personnalisé en définissant un champ
`form`, ce qui vous permet de contrôler la manière dont les champs
sont présentés lors de l'ajout ou de la modification d'un objet.

4. Actions Personnalisées :
- Vous pouvez définir des actions personnalisées que les utilisateurs
peuvent exécuter sur plusieurs objets sélectionnés dans la liste.
   
```python
class AuthorAdmin(admin.ModelAdmin):
   actions = ['make_published']

   def make_published(self, request, queryset):
       queryset.update(status='published')
       self.message_user(request, "Les auteurs sélectionnés ont été publiés.")
   make_published.short_description = "Publier les auteurs sélectionnés"
```

5. Hiérarchie des Dates :
- Avec l'option `date_hierarchy`, vous pouvez ajouter une navigation par date
à votre interface d'administration.

```python
class BookAdmin(admin.ModelAdmin):
   date_hierarchy = 'pub_date'
```

6. Groupes de Champs :
La propriété `fieldsets` dans `admin.ModelAdmin` permet de contrôler la mise
en page des formulaires d'ajout et de modification dans l'interface
d'administration de Django. Elle vous permet de regrouper les champs
en sections, ce qui améliore l'organisation et la lisibilité des formulaires.


En effet, `fieldsets` est une liste de tuples, où chaque tuple représente
un `<fieldset>` dans le formulaire d'administration. La structure
de chaque tuple est la suivante :

```python
(name, field_options)
```

- **name** : Une chaîne représentant le titre du fieldset.
Vous pouvez utiliser `None` si vous ne souhaitez pas afficher de titre.
- **field_options** : Un dictionnaire contenant des informations
sur le fieldset, notamment une liste des champs à afficher.

Voici un exemple qui illustre comment utiliser `fieldsets` pour un modèle :

```python
from django.contrib import admin
from .models import FlatPage

class FlatPageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ["url", "title", "content", "sites"],
        }),
        ("Advanced options", {
            "classes": ["collapse"],
            "fields": ["registration_required", "template_name"],
        }),
    ]

admin.site.register(FlatPage, FlatPageAdmin)
```

- Groupement des Champs :
Dans l'exemple ci-dessus, les champs `url`, `title`, `content`, et `sites`
sont regroupés dans un fieldset sans titre.
Les options avancées sont regroupées dans un autre fieldset intitulé
"Advanced options", qui est collapsible grâce à la classe `"collapse"`.

- Affichage par Défaut : Si ni `fieldsets` ni `fields` ne sont spécifiés,
Django affichera tous les champs non-autos et éditables dans un seul fieldset.

- Options Avancées : Vous pouvez également utiliser d'autres clés
dans le dictionnaire `field_options`, comme `"classes"` pour ajouter
des classes CSS personnalisées ou `"description"` pour fournir
une description pour le fieldset.

L'utilisation de `fieldsets` dans Django Admin permet de créer une interface
d'administration plus organisée et intuitive. En regroupant les champs
en sections logiques, vous améliorez l'expérience utilisateur
lors de l'ajout ou de la modification d'objets. Pour plus d'informations,
consultez la [documentation officielle de Django sur ModelAdmin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options).

### Exemple Complet

Voici un exemple complet qui montre comment configurer un modèle
avec `ModelAdmin` :

```python
from django.contrib import admin
from .models import Author, Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')
    search_fields = ('last_name', 'first_name')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre')
    list_filter = ('genre',)
    date_hierarchy = 'pub_date'
    search_fields = ('title',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
```

La classe `admin.ModelAdmin` est un outil puissant pour personnaliser
l'interface d'administration de Django. Elle vous permet de contrôler
l'affichage, la recherche, le filtrage et bien plus encore,
rendant ainsi la gestion des données beaucoup plus intuitive et efficace
pour les utilisateurs administrateurs. Pour plus d'informations détaillées,
consultez la [documentation officielle de Django sur ModelAdmin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options).

### References
- [1] https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site
- [2] https://docs.djangoproject.com/en/5.1/ref/contrib/admin/
- [3] https://docs.djangoproject.com/fr/5.1/ref/contrib/admin/
- [4] https://developer.mozilla.org/fr/docs/Learn/Server-side/Django/Admin_site
- [5] https://hodovi.cc/blog/best-practises-for-a-performant-django-admin/


## Personnalisation avec form.Form
Pour personnaliser l'interface d'administration de Django en utilisant
des formulaires (`forms`), vous pouvez créer un formulaire personnalisé
et l'associer à votre classe `ModelAdmin`. Cela vous permet de contrôler
la validation, le rendu des champs et d'ajouter des fonctionnalités
supplémentaires.

### Étapes pour utiliser des formulaires personnalisés avec ModelAdmin

1. **Créer un formulaire personnalisé** : Définissez un formulaire basé
sur `forms.ModelForm`.
2. **Associer le formulaire au ModelAdmin** : Utilisez le champ `form`
dans votre classe `ModelAdmin`.
3. **Personnaliser le comportement** : Ajoutez des méthodes pour gérer
la validation ou le rendu des champs.

### Exemple de code

#### 1. Créer un formulaire personnalisé

Voici un exemple de formulaire personnalisé pour un modèle `Book` :

```python
# forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'published_date']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Le prix ne peut pas être négatif.")
        return price
```

#### 2. Associer le formulaire au ModelAdmin

Ensuite, associez ce formulaire à votre classe `ModelAdmin` :

```python
# admin.py
from django.contrib import admin
from .models import Book
from .forms import BookForm

class BookAdmin(admin.ModelAdmin):
    form = BookForm  # Associer le formulaire personnalisé

admin.site.register(Book, BookAdmin)
```

#### 3. Personnaliser le comportement (facultatif)

Vous pouvez également personnaliser d'autres aspects du formulaire,
comme le rendu des champs ou l'ajout de méthodes supplémentaires :

```python
class BookAdmin(admin.ModelAdmin):
    form = BookForm

    def save_model(self, request, obj, form, change):
        # Vous pouvez ajouter une logique supplémentaire avant de sauvegarder
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Vous pouvez modifier le formulaire ici si nécessaire
        return form
```

En utilisant des formulaires personnalisés avec `ModelAdmin`,
vous pouvez améliorer l'interface d'administration de Django en ajoutant
une validation personnalisée, en modifiant le rendu des champs et en intégrant
une logique métier spécifique. Cela rend l'administration plus intuitive
et adaptée aux besoins de votre application. Pour plus d'informations
détaillées, consultez la [documentation officielle de Django sur les formulaires](https://docs.djangoproject.com/en/stable/topics/forms/) et sur [ModelAdmin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options).

