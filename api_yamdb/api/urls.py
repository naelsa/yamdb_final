from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, signup_user, get_token, GenresViewSet,
                    CategoriesViewSet, TitlesViewSet, ReviewViewSet,
                    CommentViewSet)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('genres', GenresViewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='Comment'
)
v1_patterns = [
    path('signup/', signup_user, name='auth_signup'),
    path('token/', get_token, name='token'),
]
urlpatterns = [
    path('v1/auth/', include(v1_patterns)),
    path('v1/', include(router_v1.urls)),
]

app_name = 'api'
