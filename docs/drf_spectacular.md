# DRF spectacular

## Introduction
Bien sûr, je vais vous expliquer en détail le fonctionnement
de `drf-spectacular`, qui est un outil puissant pour générer automatiquement
une documentation OpenAPI (anciennement Swagger)
pour vos API Django Rest Framework (DRF).

1. Vue d'ensemble de `drf-spectacular`

`drf-spectacular` est une bibliothèque qui génère automatiquement un schéma
OpenAPI 3.0 pour vos API DRF. Elle offre une grande flexibilité
et de nombreuses options de personnalisation.

2. Installation et configuration de base

a. Installation :
```
pip install drf-spectacular
```

b. Configuration dans settings.py :
```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Votre API',
    'DESCRIPTION': 'Description de votre API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

3. Fonctionnement interne

drf-spectacular fonctionne en analysant vos vues, sérialiseurs et modèles DRF pour générer un schéma OpenAPI. Voici les étapes principales :

a. Introspection des vues :
   - Analyse les classes de vues et les fonctions de vue.
   - Détermine les méthodes HTTP supportées.
   - Extrait les paramètres de l'URL.

b. Analyse des sérialiseurs :
   - Examine les champs des sérialiseurs pour déterminer la structure des données d'entrée et de sortie.
   - Déduit les types de données et les validations.

c. Génération du schéma :
   - Crée un objet de schéma OpenAPI basé sur les informations collectées.
   - Génère les définitions de composants pour les modèles et les sérialiseurs.

d. Personnalisation :
   - Applique les personnalisations définies via les décorateurs et les paramètres de configuration.

4. Utilisation de base

a. Génération du schéma :
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

5. Personnalisation avancée

a. Décorateurs pour les vues :
```python
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=InputSerializer,
    responses={200: OutputSerializer},
    description="Description détaillée de l'endpoint",
    tags=["Tag de l'endpoint"]
)
def ma_vue(request):
    ...
```

b. Personnalisation des sérialiseurs :
```python
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(
    examples=[
        {
            'name': 'Exemple 1',
            'value': {
                'field1': 'value1',
                'field2': 'value2'
            }
        }
    ]
)
class MonSerialiser(serializers.Serializer):
    ...
```

c. Personnalisation globale dans settings.py :
```python
SPECTACULAR_SETTINGS = {
    # ...
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
    'ENUM_NAME_OVERRIDES': {
        'StatusEnum': 'myapp.models.Status',
    },
}
```

6. Gestion des authentifications

`drf-spectacular` détecte automatiquement les classes d'authentification
utilisées et les inclut dans le schéma.

7. Gestion des permissions

Les permissions sont également automatiquement détectées et incluses
dans le schéma.

8. Génération de documentation pour les `ViewSets`

Pour les ViewSets, `drf-spectacular` génère automatiquement la documentation
pour toutes les actions (list, create, retrieve, update, destroy).

9. Gestion des filtres

`drf-spectacular` supporte les filtres DRF et les inclut dans la documentation.

10. Personnalisation des types de réponse

```python
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    responses={
        200: OpenApiResponse(response=OutputSerializer, description="Succès"),
        404: OpenApiResponse(description="Non trouvé")
    }
)
def ma_vue(request):
    ...
```

11. Gestion des fichiers uploadés

drf-spectacular détecte automatiquement les champs de fichiers et les documente correctement.

12. Versionnage de l'API

Vous pouvez spécifier différentes versions de votre API :

```python
@extend_schema(versions=['v1', 'v2'])
class MaVueV1(APIView):
    ...

@extend_schema(versions=['v2'])
class MaVueV2(APIView):
    ...
```

13. Tests

drf-spectacular fournit des utilitaires pour tester votre schéma :

```python
from drf_spectacular.validation import validate_schema

class TestSchema(TestCase):
    def test_schema(self):
        schema = self.client.get('/api/schema/')
        validate_schema(schema.json())
```

14. Personnalisation des exemples

```python
from drf_spectacular.utils import OpenApiExample

@extend_schema(
    examples=[
        OpenApiExample(
            'Exemple valide',
            value={'field1': 'value1', 'field2': 'value2'},
            request_only=True,
            response_only=False,
        ),
    ]
)
def ma_vue(request):
    ...
```

15. Exclusion de champs ou d'endpoints

```python
@extend_schema(exclude=True)
def vue_non_documentee(request):
    ...

class MonSerialiser(serializers.Serializer):
    champ_cache = serializers.CharField(
        help_text="Ce champ sera caché dans la documentation")

    class Meta:
        ref_name = None  # Exclut ce sérialiseur de la documentation
```

16. Génération de clients

drf-spectacular peut générer des clients API dans différents langages
à partir de votre schéma.

drf-spectacular est un outil puissant et flexible qui automatise grandement
la création de documentation pour vos API DRF. Il offre un excellent
équilibre entre la génération automatique et la personnalisation fine,
vous permettant de créer une documentation précise et complète pour votre API.


---

Pour documenter une `APIView` de manière exhaustive avec `drf_spectacular`, l'utilisation du décorateur `@extend_schema` est indispensable. Il permet de définir les métadonnées, les types de requête, les réponses de succès et, surtout, de mapper les différents cas d'erreurs.

Voici un exemple complet mettant en œuvre une vue de création de profil avec validation complexe.

---

### Configuration de la Vue

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

# 1. Définition des Serializers pour la documentation
class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    age = serializers.IntegerField(min_value=18)

class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()

# 2. Implémentation de l'APIView
class RegisterProfileView(APIView):
    
    @extend_schema(
        summary="Création d'un profil utilisateur",
        description="Cette API permet de créer un profil complet. Elle valide l'âge et l'unicité de l'email.",
        request=UserProfileSerializer,
        parameters=[
            OpenApiParameter(
                name="num_page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description=_("Page number"),
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description=_("Number of elements per page"),
            ),
        ],
        responses={
            201: OpenApiResponse(
                response=UserProfileSerializer,
                description="Profil créé avec succès",
                examples=[
                    OpenApiExample(
                        'Succès',
                        value={'username': 'mokira_dev', 'email': 'contact@consoleart.io', 'age': 25}
                    )
                ]
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Données invalides (ex: âge insuffisant)",
            ),
            403: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Permission refusée",
            ),
        },
        tags=['Utilisateurs']
    )
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            # Logique de sauvegarde ici
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```

---

### Points Clés de l'Implémentation

* **`summary` & `description**` : Indispensables pour que l'interface Swagger soit lisible par les humains.
* **`responses` avec `OpenApiResponse**` : Permet de lister chaque code HTTP (201, 400, 403, etc.) et de lui associer un Serializer spécifique pour que le schéma JSON soit généré automatiquement.
* **`OpenApiExample`** : Très utile pour fournir des données de test directement dans l'interface, facilitant le travail des développeurs frontend.
* **`tags`** : Permet de regrouper vos endpoints par thématique (ex: Auth, Products, Billing) dans la documentation.

### Pourquoi utiliser des Serializers d'erreur ?

Même si votre code renvoie parfois un simple dictionnaire, déclarer un `ErrorResponseSerializer` permet à `drf_spectacular` de générer un modèle d'objet "Error" dans la section **Schemas** en bas de page de votre documentation.

---

Pour afficher un exemple de requête directement au niveau du **Serializer**, vous avez deux approches principales. La première consiste à utiliser la classe `Meta` (plus statique), tandis que la seconde utilise des décorateurs `drf_spectacular` (plus flexible).

### 1. Utilisation de `OpenApiExample` dans la Vue (Recommandé)

C'est la méthode la plus propre car elle permet de définir plusieurs scénarios (succès, erreur de validation, cas limite) sans polluer la logique métier du serializer.

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

class RegisterProfileView(APIView):
    @extend_schema(
        request=UserProfileSerializer,
        examples=[
            OpenApiExample(
                'Exemple Valide',
                summary='Un profil standard',
                description='Exemple de données pour un utilisateur majeur.',
                value={
                    'username': 'console_art',
                    'email': 'dev@example.com',
                    'age': 30
                },
                request_only=True, # Précise que cet exemple concerne la requête
            ),
        ]
    )
    def post(self, request):
        # ... logique ...

```

---

### 2. Utilisation de `ref_name` et `example` dans le Serializer

Si vous voulez que l'exemple soit lié au composant lui-même dans le schéma OpenAPI (section "Components"), vous pouvez ajouter l'argument `example` lors de la déclaration des champs ou utiliser `extend_schema_serializer`.

```python
from drf_spectacular.utils import extend_schema_serializer

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Exemple Serializer',
            value={
                'username': 'cyber_doc',
                'email': 'mokira@tech.io',
                'age': 28
            }
        )
    ]
)
class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, help_text="Nom d'affichage")
    email = serializers.EmailField()
    age = serializers.IntegerField(min_value=18)

```

---

### Pourquoi privilégier l'une ou l'autre ?

| Méthode | Avantage | Cas d'usage |
| --- | --- | --- |
| **Via `@extend_schema**` | Permet de varier les exemples selon l'endpoint (POST vs PUT). | Documentation précise d'une route spécifique. |
| **Via `@extend_schema_serializer**` | L'exemple suit le serializer partout où il est utilisé. | Schémas globaux et réutilisables. |
| **Via `extra_kwargs**` | Très rapide à mettre en place pour un seul champ. | Préciser le format d'un seul champ (ex: format de date). |

### Astuce : Documenter les champs individuels

Pour que l'utilisateur sache exactement quoi envoyer, n'oubliez pas d'utiliser l'argument `help_text` dans vos champs de serializer. `drf_spectacular` le récupère automatiquement pour remplir la colonne "Description" dans Swagger :

```python
age = serializers.IntegerField(
    min_value=18, 
    help_text="L'utilisateur doit avoir au moins 18 ans."
)

```

Voulez-vous voir comment gérer l'authentification (JWT ou Token) dans cette même documentation pour tester vos requêtes en direct ?
