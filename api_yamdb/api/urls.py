from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, get_token,
                    regist_user, ReviewViewSet, TitleViewSet, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>[\d]{1,9})/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]{1,9})/reviews/(?P<review_id>[\d]{1,9})'
    '/comments', CommentViewSet, basename='comments'
)
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', regist_user),
    path('v1/auth/token/', get_token),
]
