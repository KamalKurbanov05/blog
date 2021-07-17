import os


from django.test import TestCase
from django.urls import reverse

from app_blog import forms, views
from djfiles.settings import BASE_DIR


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

        return super().setUp()


class RegistrationsFormFormTest(BaseTest):
    def test_valid_form(self):
        form = forms.RegistrationsForm(
            data=self.data_for_user)
        self.assertTrue(form.is_valid())

    def test_return_error(self):
        self.data_for_user['username'] = ''
        form = forms.RegistrationsForm(self.data_for_user)
        self.assertFalse(form.is_valid())


class BlogFormTest(BaseTest):
    def test_form_valid_csv(self, *args, **kwargs):
        path_csv = os.path.join(BASE_DIR, 'media', 'test_files', 'test_csv.csv')
        csv_file = os.path.join(os.path.dirname(__file__), path_csv)
        path_image = os.path.join(BASE_DIR, 'media', 'test_files', 'test_image.jpg')
        image_file = os.path.join(os.path.dirname(__file__), path_image)
        with open(csv_file) as csv:
            data = {'csv_file': csv}
            form = forms.BlogForm(data=data)
        self.assertTrue(form.is_valid())

