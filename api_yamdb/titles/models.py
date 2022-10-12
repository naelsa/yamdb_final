from django.conf import settings
from django.db import models

from .validators import validate_year


class BaseNameSlugModel(models.Model):
    """Базовый класс для категорий и жанров."""
    name = models.CharField(max_length=settings.MAX_LENGTH_TITLE_NAME)
    slug = models.SlugField(unique=True, max_length=settings.MAX_LENGTH_SLUG)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Categories(BaseNameSlugModel):
    """Категории (типы) произведений."""
    class Meta(BaseNameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(BaseNameSlugModel):
    """Категории жанров."""
    class Meta(BaseNameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения, к которым пишут отзывы."""
    name = models.CharField(max_length=settings.MAX_LENGTH_TITLE_NAME)
    year = models.IntegerField(validators=[validate_year])
    description = models.CharField(
        max_length=settings.MAX_LENGTH_DESCRIPTION, null=True
    )
    genre = models.ManyToManyField(
        Genres, related_name="titles",
        blank=True
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
