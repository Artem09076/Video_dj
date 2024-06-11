"""This module include test on file views.py."""
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from video_app.models import CustomUser, Video

OK = 200
REDIRECT = 302


class ViewTests(TestCase):
    """Test class for views file.

    Args:
        TestCase (_type_): django test case
    """

    def setUp(self):
        """Set function test."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.custom_user = CustomUser.objects.create(user=self.user)
        self.video = Video.objects.create(
            name='Test Video',
            video_file=None,
            cover_video_file=None,
            during=100,
            user=self.custom_user,
            description='Test Description',
        )

    def test_home_page(self):
        """Test views home page."""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'home_page.html')
        self.assertContains(response, 'Test Video')

    def test_users_video_catalog(self):
        """Test views user video catalog."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'catalog/videos.html')
        self.assertContains(response, 'Test Video')

    def test_user_comment_catalog(self):
        """Test views usercomments catalog."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('comments'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'catalog/comments.html')

    def test_video_view(self):
        """Test views video."""
        video_id = f'?id={self.video.id}'
        response = self.client.get(reverse('video') + video_id)
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'entities/video.html')
        self.assertContains(response, 'Test Video')

    def test_register(self):
        """Test views register."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'forms/register.html')
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'testname',
            'last_name': 'testlastname',
            'email': 'test@gmail.com',
        })
        self.assertEqual(response.status_code, REDIRECT)

    def test_log_in(self):
        """Test views login."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, OK)
        self.assertTemplateUsed(response, 'forms/login.html')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, REDIRECT)

    def test_log_out(self):
        """Test views logout."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, REDIRECT)
