from django.db import models

from user.models import User
from django.db import models


class Bookmark(models.Model):
    TYPE_CHOICES = [
        ('website', 'Website'),
        ('book', 'Book'),
        ('article', 'Article'),
        ('music', 'Music'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks',
                             blank=True, null=True, verbose_name='Закладка пользователя')
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Оглавление')
    description = models.TextField(max_length=1500, blank=True, null=True, verbose_name='Описание')
    url = models.URLField(blank=True, null=True, verbose_name='Url')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='website', verbose_name='Тип')
    image_preview = models.URLField(blank=True, null=True, verbose_name='Ссылка на изображение')
    collections = models.ManyToManyField('Collection', blank=True, null=True, verbose_name='Коллекции')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collectoins',
                            blank=True, null=True, verbose_name='Коллекция пользователя')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название')
    description = models.TextField(max_length=400, blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'