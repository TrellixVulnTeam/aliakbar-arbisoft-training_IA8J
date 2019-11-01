import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from accounts.views import RegisterAPI
from blog.models import Blog
from blog.views import BlogAPI, CommentAPI

pytestmark = pytest.mark.django_db


class BlogTests(APITestCase):
    """
    Tests for Blog.
    """
    factory = APIRequestFactory()

    def register(self, credentials):
        """
        Registers a user given the credentials for test purposes.
        """
        view = RegisterAPI.as_view()
        url = '/api/auth/register'

        request = self.factory.post(url, credentials)
        response = view(request)
        assert status.HTTP_200_OK == response.status_code
        return response

    def create_blog_request(self, create_blog_content):
        """
        Creates a Blog Post.
        """
        credentials = {
            'username': 'test',
            'email': 'abc@example.com',
            'password': '123'
        }
        self.register(credentials)
        url = '/api/blog'
        request = self.factory.post(url, create_blog_content)
        return request

    def _create_blog(self):
        create_blog_content = {
            'title': 'Test',
            'description': 'This is a Test Blog.'
        }
        request = self.create_blog_request(create_blog_content)
        user = User.objects.get(username='test')
        view = BlogAPI.as_view({
            'post': 'create'
        })
        force_authenticate(request, user=user)
        response = view(request)

        assert status.HTTP_201_CREATED == response.status_code
        return response

    def test_get_blog_list_authorized(self):
        """
        Tests to get a list of Blog Post, authorized.
        """
        credentials = {
            'username': 'test',
            'email': 'abc@example.com',
            'password': '123'
        }
        self.register(credentials)

        view = BlogAPI.as_view({
            'get': 'list'
        })
        url = '/api/blog'
        user = User.objects.get(username='test')
        request = self.factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)

        assert status.HTTP_200_OK == response.status_code

    def test_create_blog(self):
        """
        Tests to create a Blog Post Successfully.
        """
        response = self._create_blog()

        assert status.HTTP_201_CREATED == response.status_code
        assert 1 == Blog.objects.count()
        assert 'Test' == Blog.objects.get().title

    def test_create_blog_failed(self):
        """
        Tests to create a Blog Post Unsuccessfully.
        """
        create_blog_content = {
            'title': 'This is a Test Blog.'
        }
        view = BlogAPI.as_view({
            'post': 'create'
        })
        request = self.create_blog_request(create_blog_content)
        user = User.objects.get(username='test')
        force_authenticate(request, user=user)
        response = view(request)

        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_delete_blog(self):
        """
        Tests to delete a Blog Post.
        """
        self._create_blog()
        user = User.objects.get(username='test')

        blog = Blog.objects.get()
        view = BlogAPI.as_view({
            'delete': 'destroy'
        })
        url = '/api/blog'
        request = self.factory.delete(url)
        force_authenticate(request, user=user)
        response = view(request, slug=blog.slug)

        assert status.HTTP_204_NO_CONTENT == response.status_code

    def test_update_blog(self):
        """
        Tests to update a Blog Post Successfully.
        """
        self._create_blog()
        user = User.objects.get(username='test')

        blog = Blog.objects.get()
        update_blog_content = {
            'title': 'Test101',
            'description': 'This is a Test Blog. Amirite! :D'
        }
        url = '/api/blog/'
        request = self.factory.put(url, update_blog_content)
        view = BlogAPI.as_view({
            'put': 'update'
        })
        force_authenticate(request, user=user)
        response = view(request, slug=blog.slug)

        assert status.HTTP_200_OK == response.status_code
        assert 1 == Blog.objects.count()
        assert update_blog_content['title'] == Blog.objects.get().title

    def test_search_blog_list(self):
        """
        Tests to search Blog Posts Successfully.
        """
        self._create_blog()

        keyword = 'Test'
        url = '/api/blog/?keyword=%s' % keyword
        request = self.factory.get(url)
        view = BlogAPI.as_view({
            'get': 'list'
        })
        response = view(request)

        assert status.HTTP_200_OK == response.status_code
        assert 1 == response.data['count']
        assert keyword == response.data['results'][0]['title']

    def test_get_blog_list(self):
        """
        Tests to get Blog Posts Successfully.
        """
        url = '/api/blog/'
        request = self.factory.get(url)
        view = BlogAPI.as_view({
            'get': 'list'
        })
        response = view(request)

        assert status.HTTP_200_OK == response.status_code
        assert 0 == response.data['count']

    def test_blog_upvote(self):
        """
        Tests Upvote functionality.
        """
        self._create_blog()

        user = User.objects.get(username='test')
        blog = Blog.objects.get()
        url = '/api/blog/'
        request = self.factory.get(url)
        force_authenticate(request, user=user)
        view = BlogAPI.as_view({
            'get': 'upvote'
        })
        response = view(request, slug=blog.slug)

        assert status.HTTP_200_OK == response.status_code
        assert 'You have successfully up voted this blog post.' == response.data

        response = view(request, slug=blog.slug)

        assert status.HTTP_200_OK == response.status_code
        assert 'You have already up voted this blog post.' == response.data

    def test_blog_downvote(self):
        """
        Tests Downvote functionality.
        """
        self._create_blog()

        user = User.objects.get(username='test')
        blog = Blog.objects.get()
        url = '/api/blog/'
        request = self.factory.get(url)
        force_authenticate(request, user=user)
        view = BlogAPI.as_view({
            'get': 'downvote'
        })
        response = view(request, slug=blog.slug)

        assert status.HTTP_200_OK == response.status_code
        assert 'You have successfully down voted this blog post.' == response.data

        response = view(request, slug=blog.slug)

        assert status.HTTP_200_OK == response.status_code
        assert 'You have already down voted this blog post.' == response.data

    def test_post_a_comment(self):
        """
        Tests a comment is successfully posted.
        """
        response = self._create_blog()

        user = User.objects.get(username='test')
        blog = response.data['url']
        comment_content = {
            'blog': blog,
            'description': 'This is a Test Comment.'
        }
        url = '/api/comment/'
        request = self.factory.post(url, comment_content)
        force_authenticate(request, user=user)
        view = CommentAPI.as_view({
            'post': 'create'
        })
        response = view(request)

        assert status.HTTP_201_CREATED == response.status_code
        assert comment_content['description'] == response.data['description']
        assert response.data['parent'] is None

        reply_content = {
            'blog': blog,
            'description': 'This is a Test Reply.',
            'parent': response.data['id']
        }
        request = self.factory.post(url, reply_content)
        force_authenticate(request, user=user)
        response = view(request)

        assert status.HTTP_201_CREATED == response.status_code
        assert reply_content['description'] == response.data['description']
        assert reply_content['parent'] == response.data['parent']
