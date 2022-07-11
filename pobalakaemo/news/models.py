import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


class News(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default=uuid.uuid1)
    content = models.TextField(verbose_name='Текст')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Час створення')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Остання зміна')
    is_published = models.BooleanField(default=False, verbose_name='Опубліковано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категорія')
    news_author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Новини"
        verbose_name_plural = 'Новини'
        ordering = ['-time_create', 'title']



class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категорія')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['id']
