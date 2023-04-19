from django.utils.translation import gettext as _
from django.db import models


class BaseDBModel(models.Model):
    """Base database model.

    Attributs:
        created_at (datatime):
            La date de creation de l'objet dans la base de donnees.
        updated_at (datatime):
            La date de derniere mise a jour de l'objet dans
            la base de donnees.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("creation date"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("udating date"),
    )

    class Meta:
        abstract = True

    @classmethod
    @property
    def modelname(cls) -> str:
        """Retourne le nom du model."""
        return cls.__name__
