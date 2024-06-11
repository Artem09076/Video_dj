from django.test import TestCase
from django.utils import timezone
from video_app.models import Video, Comment, CustomUser
from django.contrib.auth.models import User
from datetime import datetime

class ModelTests(TestCase):
    
    def setUp(self):
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
        self.comment = Comment.objects.create(
            text='Test Comment',
            video=self.video,
            user=self.custom_user,
        )

    def test_video_creation(self):
        self.assertEqual(self.video.name, 'Test Video')
        self.assertEqual(self.video.during, 100)
        self.assertEqual(self.video.description, 'Test Description')
        self.assertEqual(self.video.user, self.custom_user)

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, 'Test Comment')
        self.assertEqual(self.comment.video, self.video)
        self.assertEqual(self.comment.user, self.custom_user)
