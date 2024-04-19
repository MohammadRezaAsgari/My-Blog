from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Post, Comment
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

class YourAppTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        self.category = Category.objects.create(name='Test Category', desc='Test Description')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user, category=self.category)
        self.comment = Comment.objects.create(content='Test Comment', author=self.user, post=self.post)



    def test_category_views(self):
        response = self.client.get(reverse('category-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'name': 'New Category', 'desc': 'New Description'}
        response = self.client.post(reverse('category-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

        category_id = response.data['id']
        response = self.client.get(reverse('category-retrieve-update-destroy', args=[category_id, ]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_data = {'name': 'Updated Category', 'desc': 'Updated Description'}
        response = self.client.put(reverse('category-retrieve-update-destroy', args=[category_id, ]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Category')

        updated_desc = {'desc': 'Updated Description Again'}
        response = self.client.patch(reverse('category-retrieve-update-destroy', args=[category_id, ]), updated_desc)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['desc'], 'Updated Description Again')

        response = self.client.delete(reverse('category-retrieve-update-destroy', args=[category_id, ]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)

    def test_post_views(self):
        response = self.client.get(reverse('post-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'title': 'New Post', 'content': 'New Content', 'category': self.category.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('post-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

        post_id = response.data['id']
        response = self.client.get(reverse('post-retrieve-update-destroy', args=[post_id, ]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_content = {'content': 'Updated Content Again'}
        response = self.client.patch(reverse('post-retrieve-update-destroy', args=[post_id, ]), updated_content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated Content Again')

        response = self.client.delete(reverse('post-retrieve-update-destroy', args=[post_id, ]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)

    def test_comment_views(self):
        response = self.client.get(reverse('comment-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'content': 'New Comment', 'post': self.post.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('comment-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

        comment_id = response.data['id']
        response = self.client.get(reverse('comment-retrieve-update-destroy', args=[comment_id, ]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_content = {'content': 'Updated Comment Again'}
        response = self.client.patch(reverse('comment-retrieve-update-destroy', args=[comment_id, ]), updated_content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated Comment Again')

        response = self.client.delete(reverse('comment-retrieve-update-destroy', args=[comment_id, ]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 1)

    def test_post_permissions(self):
        data = {'title': 'New Post', 'content': 'New Content', 'category': self.category.id}

        response = self.client.post(reverse('post-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('post-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('post-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post_id = response.data['id']
        updated_data = {'title': 'Updated Post', 'content': 'Updated Content'}
        response = self.client.patch(reverse('post-retrieve-update-destroy', args=[post_id, ]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        other_user = User.objects.create_user(username='otheruser', password='54321')
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(reverse('post-retrieve-update-destroy', args=[post_id, ]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_permissions(self):
        data = {'content': 'New Comment', 'post': self.post.id}
        response = self.client.post(reverse('comment-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('comment-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        response = self.client.post(reverse('comment-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment_id = response.data['id']
        updated_data = {'content': 'Updated Comment'}
        response = self.client.patch(reverse('comment-retrieve-update-destroy', args=[comment_id, ]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        other_user = User.objects.create_user(username='otheruser', password='54321')
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(reverse('comment-retrieve-update-destroy', args=[comment_id, ]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
