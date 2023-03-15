from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='alexa', password='pass')

    def test_can_list_posts(self):
        alexa = User.objects.get(username='alexa')
        Post.objects.create(owner=alexa, title='a title')
        response = self.client.get('/posts/')
        # make the test fail initially by using the incorrect status code
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # then test with correct code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print existing data and the number of posts (length)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='alexa', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        # check if there is 1 new post
        self.assertEqual(count, 1)
        # first make the test fail with incorrect status code
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # then pass in the correct status code as shown by test results
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        # first make the test fail with incorrect status code
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # then pass in the correct status code as shown by test results
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
