from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='titles'
    )

    class Meta:
        ordering = ['year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Обзор')
    score = models.IntegerField(verbose_name='Оценка')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Автор отзыва',
    )

    class Meta():
        ordering = ['title',]
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'


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
        related_name='comment',
        verbose_name='Обзор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
