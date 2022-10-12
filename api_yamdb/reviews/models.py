from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import Truncator

from titles.models import Title
from users.models import User


class BaseTextAuthorPubdateModel(models.Model):
    """Базовая модель."""
    text = models.TextField(
        verbose_name='Подробное название'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        verbose_name = 'Подробное название'
        verbose_name_plural = 'Подробные названия'
        ordering = ('pub_date',)

    def __str__(self):
        return Truncator(self.text).words(settings.NUMBER_WORDS_TRUNC)


class Review(BaseTextAuthorPubdateModel):
    """Отзыв"""
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MinValueValidator(1, message='Минимальная оценка 1'),
            MaxValueValidator(10, message='Максимальная оценка 10')
        ]
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )

    class Meta(BaseTextAuthorPubdateModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(BaseTextAuthorPubdateModel):
    """Комментарий к отзыву."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(BaseTextAuthorPubdateModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
