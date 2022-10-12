from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный пользователь с дополнительными полями."""
    username = models.CharField(
        max_length=settings.MAX_LENGTH_USER,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
        verbose_name='Электронная почта'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=settings.MAX_LENGTH_CONFIRMATION_CODE,
        blank=True,
        verbose_name='Код для авторизации',
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_LENGTH_NAME,
        blank=True)
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_LENGTH_NAME,
        blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    role = models.CharField(
        max_length=max(
            [len(role) for user, role in settings.USER_ROLE_CHOICES]),
        choices=settings.USER_ROLE_CHOICES,
        default=settings.USER_ROLE_USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == settings.USER_ROLE_ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == settings.USER_ROLE_MODERATOR
