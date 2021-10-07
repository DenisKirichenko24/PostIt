from django import forms
from django.forms import ModelForm
from django.forms.widgets import Textarea

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
            'image': ('Изображение')
        }
        help_texts = {
            'group': ('Необходимо выбрать группу для новой записи'),
            'text': ('Необходимо добавить текст новой записи'),
            'image': ('Необходимо загрузить изображение для новой записи')
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': Textarea}
        help_texts = {'text': ('Ваш комментарий')}

    def clean_text(self):
        comment = self.cleaned_data['text']
        if comment == '':
            raise forms.ValidationError(
                "Вы добавляете пустой комментарий")
        return comment
