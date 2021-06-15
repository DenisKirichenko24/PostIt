import tempfile

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, Follow

User = get_user_model()


class PaginatorViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        [Post.objects.create(text='а' * 100, author=self.user)
         for number in range(11)]
        self.client = Client()
        self.client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_one_record(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 1)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(dir=settings.MEDIA_ROOT))
class PostsPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')
        cls.group = Group.objects.create(title='TestGroup',
                                         description='Test description',
                                         slug='test-slug',
                                         )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(text='TestText',
                                       author=PostsPagesTests.user,
                                       group=PostsPagesTests.group,
                                       )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsPagesTests.user)
        self.follower = User.objects.create_user(
            username='test_user1',
            email='testfollower@test.ru',
            password='test_pass'
        )
        self.following = User.objects.create_user(
            username='test_user2',
            email='testfollowingg@test.ru',
            password='test_pass2'
        )

    def test_pages_uses_correct_template(self):
        templates_page_names = {
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),
            'group.html': reverse('group_posts', kwargs={'slug': 'test-slug'}),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_shows_correct_context(self):
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.context.get('page').object_list[0],
                         PostsPagesTests.post)

    def test_home_page_shows_new_post_with_group(self):
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(response.context.get('page').object_list[0],
                         PostsPagesTests.post)

    def test_new_post_shows_correct_context(self):
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_new_post_shows_correct_context_assert(self):
        response = self.authorized_client.get(reverse('post', kwargs={
            'username': 'test_user',
            'post_id': PostsPagesTests.post.id
        }))
        context_values = {
            'post': PostsPagesTests.post,
            'author': PostsPagesTests.user,
        }
        for value, expected in context_values.items():
            with self.subTest(value=value):
                self.assertEqual(response.context[value], expected)

    def test_group_page_shows_correct_context(self):
        response = self.guest_client.get(reverse(
            'group_posts', kwargs={'slug': 'test-slug'}
        ))
        self.assertEqual(response.context['group'], PostsPagesTests.group)

    def test_new_post_with_group_shows_not_in_other_group_page(self):
        response = self.guest_client.get(reverse(
            'group_posts', kwargs={'slug': 'test-slug'}
        ))
        self.assertNotEqual(response.context.get('page').object_list,
                            PostsPagesTests.post)

    def test_page_not_found(self):
        response_page_not_found = self.guest_client.get('/tests_url/')
        self.assertEqual(response_page_not_found.status_code, 404)

    def test_follow(self):
        self.client.force_login(self.follower)
        self.post = Post.objects.create(text='Test follow',
                                        author=self.following)
        resp = self.client.get(f'/{self.follower}/follow/')
        resp = Follow.objects.filter(user=self.follower).exists()
        self.assertFalse(resp)

    def test_unfollow(self):
        self.client.force_login(self.follower)
        self.post = Post.objects.create(text='Test unfollow',
                                        author=self.following)
        resp = self.client.get(f'/{self.following}/unfollow/')
        resp = Follow.objects.filter(user=self.follower).exists()
        self.assertFalse(resp)
