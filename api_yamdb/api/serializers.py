from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.core.validators import RegexValidator
from django.db.models import Avg

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        rating = (obj.review.aggregate(Avg('score'))
                  .get('score__avg', None)
                  )
        return round(rating) if rating is not None else None


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        return TitleSerializer(instance, context=self.context).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Проверка на повторную публикацию отзыва"""

        request = self.context.get('request')
        if request is None and not hasattr(request, 'user'):
            raise serializers.ValidationError(
                'Возникла ошибка при обработке запроса: '
                'не удалось извлечь автора отзыва.')
        view = self.context.get('view')
        if view is None:
            raise serializers.ValidationError(
                'Возникла ошибка при обработке запроса: '
                'не удалось извлечь объект view.')
        title_id = view.kwargs.get('title_id')
        if title_id is None:
            raise serializers.ValidationError(
                'Возникла ошибка при обработке запроса: '
                'не удалось извлечь title_id из запроса.')
        review = Review.objects.filter(title__id=title_id,
                                       author=request.user)
        if review.exists() and request.method == 'POST':
            raise serializers.ValidationError(
                'Вы уже опубликовали отзыв к этой публикации!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class RegistrUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя (me) в качестве username запрещено.'
            )
        return value


class TokenUserSerializer(serializers.Serializer):
    """Сериализатор для работы с токеном."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class ProfileUserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с личными данными поьзователя."""
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
