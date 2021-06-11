from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.user = User.objects.create(username='test_user')
        self.group = Group.objects.create(title='Test group')
        self.post = Post.objects.create(
            text='а' * 100,
            author=self.user
        )

    def test_post_is_title_field_length15(self):
        """В поле ___str___ объекта post правильное
        значение поля post.text."""
        post = self.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

    def test_group_title_str(self):
        """Названия группы совпадают"""
        group = PostModelTest.group
        title = str(group)
        self.assertEqual(title, group.title)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.group = Group.objects.create(title='Ш')

    def test_group_is_title_field(self):
        """В поле ___str___ объекта group правильное
        значение поля group.title."""
        group = self.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))
