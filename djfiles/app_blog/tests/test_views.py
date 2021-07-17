import os

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from app_blog import views, forms, models
from djfiles.settings import BASE_DIR


# USER_PASSWORD = 'test12345'


# https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.username = 'test_username'
        self.password = 'test_password'
        self.data_for_user = {
            'username': 'test_username',
            'email': 'test@mail.com',
            'password1': 'password_test',
            'password2': 'password_test',
            'name': 'test_name',
        }

        self.data_for_blog = {
            'title': 'test_title',
            'content': 'test_content',
        }
        self.data_for_profile = {
            'name': 'test_name',
            'about_me': 'test_test_test'
        }
        self.csv_file = os.path.join('')
        return super().setUp()


class RegistrationsViewTest(BaseTest):
    def test_get_and_template(self):
        response = self.client.get(reverse('registrations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/registrations.html')

    def test_registrations_user(self):
        response = self.client.post(reverse('registrations'), self.data_for_user)
        self.assertTrue(User.objects.get(username='test_username').is_authenticated)
        self.assertRedirects(response, expected_url=reverse('blog'))

    def test_create_profile(self):
        response = self.client.post(reverse('registrations'), self.data_for_user)
        self.assertTrue(models.Profile.objects.get(user=1, name='test_name'))
        self.assertRedirects(response, expected_url=reverse('blog'))

    def test_add_avatar(self):
        path_image = os.path.join(BASE_DIR, 'media', 'test_files', 'test_image.jpg')
        user = User.objects.create_user(self.username)
        self.client.force_login(user)
        profile = models.Profile.objects.create(user=user, name=self.data_for_user['name'])
        path = os.path.join(os.path.dirname(__file__), path_image)
        register_url = reverse('registrations')
        with open(path, 'rb') as file:
            uploaded_file = SimpleUploadedFile(name='test_image.jpg', content=file.read(),
                                               content_type='image/jpg')
        self.data_for_user['avatar'] = uploaded_file
        self.client.post(register_url, self.data_for_user, {'avatar': uploaded_file})
        self.assertTrue(models.Avatar.objects.filter(id=1).exists())


class AuthenticatedTest(BaseTest):
    def test_get_auth_and_valid_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/login.html')

    def test_authenticated(self):
        username = 'test_user'
        password = 'test12345'
        User.objects.create_user(username=username, password=password)
        response = self.client.post(
            reverse('login'),
            {'username': username, 'password': password},
            follow=True,
        )
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, reverse('blog'))


class LogoutTest(BaseTest):
    def test_get_and_template(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/logout.html')

    def test_exit_from_profile(self):
        user = User.objects.create_user(username=self.username)
        self.client.force_login(user)
        response = self.client.post(reverse('logout'))
        self.assertFalse(response.context['user'].is_authenticated)


class CreateBlogTest(BaseTest):
    def test_get_and_template(self):
        response = self.client.get(reverse('create_blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/create_blog.html')

    def test_create_blog(self):
        user = User.objects.create_user(self.username)
        self.client.force_login(user)
        response = self.client.post(reverse('create_blog'), self.data_for_blog)
        self.assertTrue(models.Blog.objects.get(user=1, title='test_title'))
        self.assertRedirects(response, reverse('blog'))


class CreateBlogWithCsvTest(BaseTest):
    def test_get_template(self):
        response = self.client.get(reverse('create_blog_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/create_blog_csv.html')

    def test_create_blog_csv(self):
        csv_path = os.path.join(BASE_DIR, 'media', 'test_files', 'test_csv.csv')
        user = User.objects.create_user(self.username)
        self.client.force_login(user)
        url = reverse('create_blog_csv')
        path = os.path.join(os.path.dirname(__file__), csv_path)
        with open(path) as csv:
            self.client.post(url, {'csv_file': csv})
        self.assertTrue(models.Blog.objects.get(user=1, content='test_content'))


class BlogListTest(BaseTest):
    def test_get_template(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/blog_list.html')

    def test_list_blog(self):
        user = User.objects.create_user(username=self.username)
        self.data_for_blog['user'] = user
        models.Blog.objects.create(**self.data_for_blog)
        models.Blog.objects.create(**self.data_for_blog)
        self.assertEqual(len(views.BlogList.queryset), 2)


class BlogDetailTest(BaseTest):
    def test_get_and_template(self):
        user = User.objects.create_user(self.username)
        self.data_for_blog['user'] = user
        blog = views.Blog.objects.create(**self.data_for_blog)
        response = self.client.get(f'/blog/{blog.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/blog_detail.html')

    def test_title(self):
        blog = views.Blog.objects.create(**self.data_for_blog)
        response = self.client.get(f'/blog/{blog.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/blog_detail.html')
        self.assertTrue(blog.title)
        self.assertTrue(blog.content)


class UserDetailTest(BaseTest):
    def test_get_and_template(self):
        user = User.objects.create_user(self.username)
        response = self.client.get(f'/user/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/user_detail.html')

    def test_get_user_information(self):
        user = User.objects.create_user(self.username)
        self.data_for_profile['user'] = user
        models.Profile.objects.create(**self.data_for_profile)
        response = self.client.get(f'/user/{user.id}')
        self.assertTrue(user.profile.name)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_blog/user_detail.html')
