from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from video_app.models import Video, Comment


def create_api_test(model_class, url, creation_attrs):
    class ApiTest(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = User(username='user', password='user')
            self.superuser = User(username='admin', password='admin', is_superuser=True)
            self.user_token = Token(user=self.user)
            self.superuser_token = Token(user=self.superuser)

        def api_methods(
                self, user: User, token: Token,
                post_exp: int, put_exp: int, delete_exp: int,
        ):
            self.client.force_authenticate(user=user, token=token)

            # create model object
            self.created_id = model_class.objects.create(**creation_attrs).id
            instance_url = f'{url}{self.created_id}/'

            self.assertEqual(self.client.options(url).status_code, status.HTTP_200_OK)

            self.assertEqual(self.client.head(url).status_code, status.HTTP_200_OK)

            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)

            self.assertEqual(self.client.get(instance_url).status_code, status.HTTP_200_OK)

            self.assertEqual(self.client.get(instance_url).status_code, status.HTTP_200_OK)

            self.assertEqual(self.client.post(url, creation_attrs).status_code, post_exp)

            self.assertEqual(self.client.put(instance_url, creation_attrs).status_code, put_exp)

            self.assertEqual(self.client.delete(instance_url).status_code, delete_exp)

        def test_superuser(self):
            self.api_methods(
                self.superuser, self.superuser_token,
                status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT
            )

        def test_user(self):
            self.api_methods(
                self.user, self.user_token,
                status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN
            )

    return ApiTest

BookApiTest = create_api_test(Video, '/api/videos/', {'name': 'A', 'during': 1, 'date_publication': timezone.now()})
GenreApiTest = create_api_test(Comment, '/api/comments/', {'text': 'A', 'count_likes': 2, 'date_publication': timezone.now()})
