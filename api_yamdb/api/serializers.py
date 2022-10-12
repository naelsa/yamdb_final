from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, Review
from titles.models import Title, Categories, Genres
from titles.validators import validate_year
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        fields = (
            'username', 'email', 'bio', 'first_name', 'last_name', 'role',
        )
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    """Запрещает редактировать роль пользователю"""

    class Meta:
        fields = (
            'username', 'email', 'bio', 'first_name', 'last_name', 'role',
        )
        model = User
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True
    )

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate_username(self, data):
        if data.lower() == 'me':
            raise serializers.ValidationError('Имя не может быть "me".')
        return data


class RegTokSerializer(serializers.Serializer):
    """Сериализатор токена."""
    username = serializers.CharField(max_length=settings.MAX_LENGTH_USER,
                                     required=True)
    confirmation_code = serializers.CharField(
        max_length=settings.MAX_LENGTH_CONFIRMATION_CODE,
        required=True)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        exclude = ("id",)
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        exclude = ("id",)
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, )
    category = CategoriesSerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category')
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitlesCreateSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(validators=[
        MinValueValidator(1, message='Минимальная оценка 1'),
        MaxValueValidator(10, message='Максимальная оценка 10')
    ])

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        current_title = get_object_or_404(
            Title, pk=request.parser_context['kwargs'].get('title_id')
        )
        if current_title.reviews.filter(author=request.user).exists():
            raise serializers.ValidationError(
                'Вы не можете добавить более одного отзыва на произведение'
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
