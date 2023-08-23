from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from .models import Blog


class BlogAPITest(APITestCase):
    def setUp(self):
        creds = [{
            'username': 'testuser1',
            'password': 'testpassword1'
        },
            {
            'username': 'testuser2',
            'password': 'testpassword2'
        }]
        self.user1 = User.objects.create_user(**creds[0])
        self.user2 = User.objects.create_user(**creds[1])
        self.client1 = APIClient()
        self.client2 = APIClient()

        # get the JWT token
        response = self.client1.post('/api/token/', creds[0], format='json')
        self.token = response.data['access']
        self.client1.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client2.post('/api/token/', creds[1], format='json')
        self.token = response.data['access']
        self.client2.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_blog(self):
        response = self.client2.post('/api/blogs/', {
            'title': 'Test Blog',
            'author': self.user2.id,
            'description': 'This is a test blog description.',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.get().title, 'Test Blog')

    def test_get_blog_list(self):
        Blog.objects.create(title='Blog 1', author=self.user2)
        Blog.objects.create(title='Blog 2', author=self.user2)
        response = self.client2.get('/api/blogs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_blog_detail(self):
        blog = Blog.objects.create(title='Test Blog', author=self.user2)
        response = self.client2.get(f'/api/blogs/{blog.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Blog')

    def test_update_blog(self):
        blog = Blog.objects.create(title='Old Title', author=self.user2)
        response = self.client2.put(f'/api/blogs/{blog.id}/', {
            'title': 'New Title',
            'author': self.user2.id,
            'description': 'Updated description.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Blog.objects.get(id=blog.id).title, 'New Title')

    def test_delete_blog(self):
        blog = Blog.objects.create(title='Test Blog', author=self.user2)
        response = self.client2.delete(f'/api/blogs/{blog.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Blog.objects.count(), 0)

    def test_delete_other_user_blog(self):
        blog = Blog.objects.create(title='Test Blog', author=self.user2)
        response = self.client1.delete(f'/api/blogs/{blog.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Blog.objects.count(), 1)

    def test_update_other_user_blog(self):
        blog = Blog.objects.create(title='Old Title', author=self.user2)
        response = self.client1.put(f'/api/blogs/{blog.id}/', {
            'title': 'New Title',
            'author': self.user2,
            'description': 'Updated description.',
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Blog.objects.count(), 1)

    def test_post_unauthenticated_user(self):
        client = APIClient()
        response = client.post('/api/blogs/', {
            'title': 'Test Blog',
            'author': self.user1.id,
            'description': 'This is a test blog description.',
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Blog.objects.count(), 0)
