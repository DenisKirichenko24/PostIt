from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название сообщества')
    slug = models.SlugField(max_length=300,
                            unique=True, verbose_name='Адрес')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')

    class Meta:
        ordering = ['title']
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title


class Post(models.Model):
    group = models.ForeignKey(Group, null=True, blank=True,
                              verbose_name='Сообщество',
                              related_name='group_posts',
                              on_delete=models.SET_NULL)
    text = models.TextField(verbose_name='Содержание публикации')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='posts')
    image = models.ImageField(upload_to='posts/', blank=True, null=True,
                              verbose_name='Изображение')

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comment',
                             verbose_name='Пост')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author_comment',
                               verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата и время комментария')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    def __str__(self):
        return self.text
