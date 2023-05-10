## PostGIS
1. For using a *spacial database*, we can install the following extension:

###### `>_ cmd@01:~$`
```sh
# PostGIS is an extension of PostgreSQL
# that allows to process the spacial data like the Polygons,
# the Points, ...
sudo apt install postgis
```

2. And then, we must to connect to the application database,
here nammed `cbrdb` and create the `postgis` extensions on it.

###### `</> SQL [01]`
```sql
-- connect to cbrdb.
\c cbrdb;

-- Only you are using a spatial database
CREATE EXTENSION postgis;
```

3. Create a django database model like following:

###### `</> PYTHON [01]`
```python
# from django.db import models
from django.contrib.gis.db import models


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the
    # attributes in the world borders shapefile.
    name = models.CharField(max_length=50, unique=True)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        """Representation in string.
        Returns:
            str: return a string like France (34.453, -8.9877)
        """
        return "{} ({}, {})".format(self.name, self.lat, self.lon)

```

> **NOTE**: If you use a spacial database, you must use
> `django.contrib.gis.db` inside of `django.db`.

4. Create a new file named `load.py` into your package application and write
the following source code:

###### `</> PYTHON [02]`
```python
"""Data loading module.

.. _For more information on this file, see:
https://docs.djangoproject.com/en/4.1/ref/contrib/gis/tutorial/#layermapping
"""

from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import WorldBorder


WORLD_MAPPING = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'mpoly': 'MULTIPOLYGON',
}
WORLD_SHP = Path(__file__).resolve().parent / 'data'\
     / 'TM_WORLD_BORDERS-0.3.shp'


def run(verbose=True):
    """Function of data loading into database.

    Args:
        verbose (bool): Specifies if the loading process 
            will be verbose or not.
    """
    lm = LayerMapping(WorldBorder, WORLD_SHP, WORLD_MAPPING, transform=False)
    lm.save(strict=True, verbose=verbose)

```
