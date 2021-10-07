from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='tester')
        cls.user2 = User.objects.create_user(username='tester2')
        cls.group = Group.objects.create(title='Test group',
                                         description='Test description',
                                         slug='test-slug',)
        cls.post = Post.objects.create(
            text='test_post',
            author=PostsURLTests.user
        )
        cls.urls = ['/', '/group/test-slug/', '/new/', '/tester/',
                    '/tester/1/']

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsURLTests.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(PostsURLTests.user2)
        self.post_edit = '/tester/1/edit/'

    def test_server_return_404(self):
        """Тестовый сервер возвращает страницу ошибки."""
        tests_url = '/tests_url/'
        response = self.guest_client.get(tests_url)
        self.assertEqual(response.status_code, 404)

    def test_urls_exists_at_desired_location(self):
        """URL соответствуют адресам."""
        for url in PostsURLTests.urls[:2]:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_new_post_url_exists_at_desired_location(self):
        """Новый пост URL находится по корректному адресу."""
        response = self.authorized_client.get(PostsURLTests.urls[2],
                                              follow=True)
        self.assertEqual(response.status_code, 200)

    def test_new_post_url_redirect_anonymous_on_login(self):
        """Создание поста редиректит неавторизованного
        пользователя на страницу логина."""
        response = self.guest_client.get(PostsURLTests.urls[2],
                                         follow=True)
        login_new_url = '/auth/login/?next=/new/'
        self.assertRedirects(response, login_new_url)

    def test_post_edit_url_doesnt_show_for_anonymous(self):
        """Редактирование поста не показывается
        неавторизованному пользователю."""
        response = self.guest_client.get(self.post_edit)
        self.assertNotEqual(response.status_code, 200)

    def test_post_edit_url_shows_for_author(self):
        """Редактирование поста показывается только автору поста."""
        response = self.authorized_client.get(self.post_edit)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_url_doesnt_show_for_notauthor(self):
        response = self.authorized_client2.get(self.post_edit)
        self.assertNotEqual(response.status_code, 200)

    def test_post_edit_url_redirect_anonymous_on_login(self):
        """Редактирование поста не показывается неавтору."""
        login_tester_url = '/auth/login/?next=/tester/1/edit/'
        response = self.guest_client.get(self.post_edit, follow=True)
        self.assertRedirects(response, login_tester_url)

    def test_post_edit_url_redirect_notauthor_on_post_url(self):
        """Редактирование поста редиректит неавтора на страницу поста."""
        tester_url = '/tester/1/'
        response = self.authorized_client2.get(self.post_edit, follow=True)
        self.assertRedirects(response, tester_url)

    def test_urls_uses_correct_template(self):
        """URL используют соответствующий шаблон."""
        templates_url_names = {
            '/': 'index.html',
            '/group/test-slug/': 'group.html',
            '/new/': 'new.html',
            '/tester/1/edit/': 'new.html'
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
