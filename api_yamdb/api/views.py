from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Review, Title
from titles.models import Genres, Categories
from users.models import User

from .filters import TitleFilter
from .generate_code import send_mail_to_user
from .mixins import CreateListDestroyViewSet
from .permissions import (IsAuthorModeratorAdminSuperuser,
                          IsAdminOrReadOnly, IsAdmin)
from .serializers import (
    UserSerializer, RegistrationSerializer, RegTokSerializer,
    CommentsSerializer, ReviewsSerializer, TitlesSerializer,
    TitlesCreateSerializer, GenresSerializer, CategoriesSerializer,
    UserEditSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['get', 'patch'],
            detail=False,
            url_path='me',
            permission_classes=[IsAuthenticated],
            serializer_class=UserEditSerializer)
    def user_me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def signup_user(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, _ = User.objects.get_or_create(
        username=username,
        email=email
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail_to_user(email, confirmation_code)
    return Response(serializer.data,
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = RegTokSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data.get('username'))
    confirmation_code = serializer.data.get('confirmation_code')
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user.is_active = True
    user.save()
    serializer.save()
    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)}, status=status.HTTP_200_OK
    )


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return TitlesSerializer
        return TitlesCreateSerializer


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorModeratorAdminSuperuser,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorModeratorAdminSuperuser,)

    def get_review(self):
        return get_object_or_404(
            Review.objects.filter(pk=self.kwargs.get('review_id')))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
