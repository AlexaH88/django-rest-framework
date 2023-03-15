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


class PostDetailViewTests(APITestCase):
    def setUp(self):
        alexa = User.objects.create_user(username='alexa', password='pass')
        adam = User.objects.create_user(username='adam', password='pass')
        Post.objects.create(
            owner=alexa, title='a title', content='alexas content'
        )
        Post.objects.create(
            owner=adam, title='another title', content='adams content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        # first test to fail
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # then test to pass
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        # first test to fail
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # then test to pass
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='alexa', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        # first test to fail
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # then test to pass
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='alexa', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        # first test to fail
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # then test to pass
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
