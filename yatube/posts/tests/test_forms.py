from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')
        cls.group = Group.objects.create(title='Test Group',
                                         description='Test description',
                                         slug='test-slug',
                                         )
        cls.post = Post.objects.create(text='а' * 5,
                                       author=PostFormTests.user,
                                       group=cls.group)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_post_form_create_new_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': self.post.text,
            'group': self.group.id,
            'author': self.user,
        }
        self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        new_post = Post.objects.first()
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(new_post.text, form_data['text'])
        self.assertEqual(new_post.id, form_data['group'])
        self.assertEqual(new_post.author, form_data['author'])

    def test_post_form_doesnt_create_new_post_guest_user(self):
        form_data = {
            'text': 'Текст поста',
            'group': self.group.id,
        }
        response = self.guest_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True)
        r_login = reverse('login')
        r_new = reverse('new_post')
        self.assertRedirects(
            response, f'{r_login}?next={r_new}')

    def test_post_form_new_post_not_added(self):
        posts_count = Post.objects.count()
        self.assertNotEqual(posts_count, posts_count + 1)

    def test_post_form_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {'text': 'Измененный текст поста'}
        self.authorized_client.post(
            reverse('post_edit', kwargs={
                'username': 'test_user',
                'post_id': PostFormTests.post.id
            }),
            data=form_data,
            follow=True
        )
        edit_post = PostFormTests.post.id
        self.assertEqual(Post.objects.get(id=edit_post).text,
                         form_data['text'])
        self.assertEqual(Post.objects.count(), posts_count)
