from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_score, validate_year


class Genre(models.Model):
    """Модель Жанров"""

    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Category(models.Model):
    """Модель Категорий"""

    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель Произведений"""

    name = models.CharField('Название произведения', max_length=100)
    year = models.PositiveSmallIntegerField(
        'Год публикации',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='titles',
        verbose_name='Категория_произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name='Описание произведения'
    )
    description = models.CharField(
        'Описание произведения',
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Модель пользователей"""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Review(models.Model):
    """Модель Отзывов к Произведениям"""

    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )

    score = models.PositiveSmallIntegerField(
        'Оценка автора отзыва',
        validators=(validate_score,)
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Отзыв к произведению'
        verbose_name_plural = 'Отзывы к произведениям'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='only_one_follow_is_possible')
        ]

    def __str__(self) -> str:
        return self.text[:settings.TEXT_VISIBLE_SYMBOLS]


class Comment(models.Model):
    """Модель Комментариев к Отзывам"""
    text = models.CharField(
        'Комментарий к отзыву',
        max_length=1200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзывам'
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.text[:settings.TEXT_VISIBLE_SYMBOLS]
