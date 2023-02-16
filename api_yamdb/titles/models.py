from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['slug', ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['slug', ]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        ordering = ['year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'], name='GenreTitle'
            )
        ]

    def __str__(self):
        return f'Это произведение {self.title} жанра {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Обзор')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )

    class Meta:
        ordering = ['title', ]
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        # constraints = [
        #     models.UniqueConstraint(fields=['author', 'title'], name='unique_review')
        # ]


class Comment(models.Model):
    text = models.TextField(verbose_name='Коментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Автор отзыва',
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
