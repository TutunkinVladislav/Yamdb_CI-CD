from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ProfileUserSerializer,
                          RegistrUserSerializer, ReviewSerializer,
                          TitleCreateSerializer, TokenUserSerializer,
                          UserSerializer)
from .permissions import (IsAdminSuperuserOrReadOnly, IsAuthOrAdmin,
                          IsAuthorAdminModeratorOrReadOnly)
from reviews.models import Category, Genre, Review, Title, User


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями"""

    queryset = Title.objects.all()
    permission_classes = (IsAdminSuperuserOrReadOnly,)
    serializer_class = TitleCreateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для работы с жанрами"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для работы с категориями"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
    """Вьюсет для работы с отзывами"""

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title_obj = get_object_or_404(Title, pk=title_id)
        return title_obj

    def get_queryset(self):
        title = self.get_title()
        queryset = title.review.all()
        return queryset

    def perform_create(self, serializer):
        title = self.get_title()
        author = self.request.user
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
    """Вьюсет для работы с комментариями к отзывам"""

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review_obj = get_object_or_404(Review,
                                       pk=review_id,
                                       title__id=title_id)
        return review_obj

    def get_queryset(self):
        review = self.get_review()
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = self.get_review()
        author = self.request.user
        serializer.save(author=author, review=review)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
        serializer_class=ProfileUserSerializer,
    )
    def profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def regist_user(request):
    """Регистрация пользователей"""

    serializer = RegistrUserSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(
            User, username=serializer.validated_data["username"]
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Код подтверждения для получения '
                    f'токена {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение токена"""

    serializer = TokenUserSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User, username=serializer.validated_data["username"]
        )
        if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
