from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validate

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='категория')
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='жанр')
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=255, verbose_name='произведение')
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[year_validate],
        verbose_name='год выхода',
        db_index=True,
    )

    description = models.TextField(null=True, blank=True,
                                   verbose_name='описание'
                                   )
    genre = models.ManyToManyField(Genre,
                                   blank=True,
                                   related_name='genre_titles',
                                   verbose_name='жанр произведения')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='category_titles',
                                 verbose_name='категория произведения')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    text = models.TextField(verbose_name='Отзыв', null=True, blank=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,

    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.id} обзор на {self.title} от {self.author}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        null=False,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.id} комментарий на {self.review} от {self.author}'
