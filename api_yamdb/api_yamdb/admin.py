from django.contrib import admin

from reviews.models import Review, Comment
from titles.models import Categories, Genres, Title
from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Администрирование пользователя."""

    list_display = ('username', 'email', 'bio', 'first_name', 'last_name',)
    search_fields = ('username', 'email', 'role',)
    list_filter = ('role',)


class ReviewAdmin(admin.ModelAdmin):
    """Администрирование отзывов."""
    list_display = ('author', 'score', 'title', 'pub_date',)
    search_fields = ('title',)
    list_filter = ('author', 'title',)


class CommentAdmin(admin.ModelAdmin):
    """Администрирование комментариев."""
    list_display = ('author', 'text', 'review', 'pub_date',)
    search_fields = ('review',)
    list_filter = ('author', 'review',)


class CategoriesAdmin(admin.ModelAdmin):
    """Администрирование категорий."""
    list_display = ('name', 'slug',)
    search_fields = ('slug',)
    list_filter = ('slug',)


class GenresAdmin(admin.ModelAdmin):
    """Администрирование жанров."""
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


class TitleAdmin(admin.ModelAdmin):
    """Администрирование произведений."""
    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name', 'year',)
    list_filter = ('year', 'genre', 'category',)


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Title, TitleAdmin)
