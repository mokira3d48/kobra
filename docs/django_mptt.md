# Django MPTT
Cette erreur est liée à l'utilisation de django-mptt (Modified Preorder Tree Traversal) qui est utilisé pour gérer des structures arborescentes dans Django. Les champs `lft` et `rght` sont des champs spéciaux utilisés par MPTT pour maintenir l'ordre hiérarchique.

Voici comment vous pouvez résoudre ce problème :

1. Vérifiez que votre fichier fixture YAML contient les champs `lft` et `rght`. Ces champs sont requis pour MPTT. Voici un exemple de structure correcte :

```yaml
- model: services.Service
  pk: 1
  fields:
    name: "Nom du service"
    # autres champs...
    tree_id: 1
    level: 0
    lft: 1
    rght: 2
    parent: null  # ou l'ID du parent si c'est un enfant
```

2. Si vous générez vos fixtures à partir de données existantes, assurez-vous d'utiliser la bonne commande :

```bash
python manage.py dumpdata services.Service --indent 2 > service_info.yaml
```

3. Si vous écrivez manuellement vos fixtures, vous devez respecter ces règles pour les valeurs MPTT :
- `lft` doit être inférieur à `rght`
- Pour un nœud racine : `level = 0`
- Les valeurs `lft` et `rght` doivent être uniques dans le même `tree_id`

4. Alternative : si c'est possible, vous pouvez aussi désactiver temporairement MPTT pendant le chargement des fixtures :

```python
from mptt.models import MPTTModel

def load_fixture():
    MPTTModel._meta.get_field('level').null = True
    MPTTModel._meta.get_field('lft').null = True
    MPTTModel._meta.get_field('rght').null = True
    # Charger la fixture
    # Puis reconstruire l'arbre
    Service.objects.rebuild()
```

## Les champs tree_id, level, lft et rght
Les champs `tree_id`, `level`, `lft`, `rght` sont gérés automatiquement par django-mptt. Voici comment ils fonctionnent :

1. `tree_id` : 
   - Identifie l'arbre auquel appartient le nœud
   - Chaque arbre racine distinct obtient un `tree_id` unique
   - Tous les descendants d'une racine partagent le même `tree_id`

2. `level` :
   - Indique la profondeur du nœud dans l'arbre
   - La racine a `level = 0`
   - Les enfants directs ont `level = 1`
   - Les petits-enfants ont `level = 2`, etc.

3. `lft` (gauche) et `rght` (droite) :
   - Utilisent l'algorithme "Modified Preorder Tree Traversal"
   - Chaque nœud a une valeur `lft` et `rght`
   - Pour un nœud donné :
     - `lft` est inférieur à tous ses descendants
     - `rght` est supérieur à tous ses descendants
     - `rght` > `lft`

Exemple concret :
```
            A              tree_id=1
           / \            A: lft=1, rght=6, level=0
          B   C          B: lft=2, rght=3, level=1
              |          C: lft=4, rght=5, level=1
```

Pour laisser MPTT gérer ces valeurs automatiquement, vous pouvez :

1. Créer vos objets sans spécifier ces champs :
```python
root = Service.objects.create(name="Service A")
child = Service.objects.create(name="Service B", parent=root)
```

2. Si vous devez reconstruire l'arbre :
```python
Service.objects.rebuild()
```

3. Pour déplacer un nœud :
```python
node.parent = new_parent
node.save()  # MPTT met à jour automatiquement tous les champs
```

En général, il est préférable de laisser MPTT gérer ces valeurs plutôt que de les définir manuellement,
sauf dans des cas très spécifiques comme la création de fixtures.

