from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from title.models import Category, Genre, Review, Title
from title.serializers import (
    ReviewSerializer,
    TitleSerializer,
    GenreSerializer
)

User = get_user_model()


class GenresApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_username',
            email='dsfd')
        self.genre_1 = Genre.objects.create(
            name='test genre 1',
            slug='genre_1')
        self.genre_2 = Genre.objects.create(
            name='test genre 2',
            slug='genre_2')

    def test_get(self):
        """Получаем список всех жанров."""
        url = reverse('genres-list')
        genres = Genre.objects.all()
        response = self.client.get(url)
        serializer_data = GenreSerializer(genres, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        """Создание нового жанра."""
        self.assertEqual(2, Genre.objects.all().count())
        data = {
            'name': 'Python 3',
            'slug': 'python',
        }
        self.client.force_login(self.user)
        url = reverse('genres-list')
        response = self.client.post(url, data=data, )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Genre.objects.all().count())
        new_genre = Genre.objects.all().first()
        self.assertEqual('Python 3', new_genre.name)
        self.assertEqual('python', new_genre.slug)

    def test_delete(self):
        """Удалить жанр."""
        self.staff_user = User.objects.create(username='test_staff_user',
                                              is_staff=True)

        self.assertEqual(2, Genre.objects.all().count())
        url = reverse('genres-detail', args=(self.genre_1.slug,))
        self.client.force_login(self.staff_user)
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Genre.objects.all().count())


class TitleApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.genre_1 = Genre.objects.create(
            name='test genre 1', slug='genre_1')
        self.genre_2 = Genre.objects.create(
            name='test genre 2', slug='genre_2')
        self.genres = Genre.objects.filter(
            id__in=(self.genre_1.id, self.genre_2.id,)
        )
        self.category_1 = Category.objects.create(
            name='test cat 1', slug='cat_1')
        self.category_2 = Category.objects.create(
            name='test cat 2', slug='cat_2')

        self.title = Title.objects.create(
            name='Test Title',
            year='2000',
            description='',
            category=self.category_1,
        )
        self.title.genre.set(self.genres)

    def test_get(self):
        """Получаем список всех title."""
        url = reverse('titles-list')
        titles = Title.objects.all()
        response = self.client.get(url)
        serializer_data = TitleSerializer(titles, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        """Создание нового title."""
        self.assertEqual(1, Title.objects.all().count())
        data = {'name': 'Поворот туда', 'year': '2000',
                'genre': [self.genre_1.slug, self.genre_2.slug],
                'category': self.category_1.slug,
                'description': 'Крутое пике'}
        url = reverse('titles-list')
        self.client.force_login(self.user)
        response = self.client.post(url, data=data)
        data['id'] = response.json()['id']
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Title.objects.all().count())
        new_title = Title.objects.all().first()
        # serializer_data = TitleSerializer(new_title).data
        self.assertEqual('Поворот туда', new_title.name)
        self.assertEqual(2000, new_title.year)

    def test_update_patch(self):
        """Обновить поля Title."""
        url = reverse('titles-detail', args=(self.title.id,))
        data = {
            'category': self.category_2.slug,
            'name': 'Test NAME',
            'genre': self.genre_1.slug
        }
        self.client.force_login(self.user)
        response = self.client.patch(url, data=data, )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.title.refresh_from_db()
        self.assertEqual(self.category_2, self.title.category)
        response_category = response.data['category']['slug']
        self.assertEqual(self.category_2.slug, response_category)
        self.assertEqual('Test NAME', self.title.name)
        response_genre = response.data['genre'][0]['slug']
        self.assertEqual(self.genre_1.slug, response_genre)


class ReviewApiTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='test_username_1',
                                          email='test1@mail.ru', )
        self.user_2 = User.objects.create(username='test_username_2',
                                          email='test2@mail.ru', )
        self.user_staff = User.objects.create(
            username='test_username_staff',
            email='test@mail.ru',
            is_staff=True,
        )

        self.genre_1 = Genre.objects.create(
            name='test genre 1', slug='genre_1')
        self.genre_2 = Genre.objects.create(
            name='test genre 2', slug='genre_2')
        self.genres = Genre.objects.filter(
            id__in=(self.genre_1.id, self.genre_2.id,)
        )
        self.category_1 = Category.objects.create(
            name='test cat 1', slug='cat_1')
        self.category_2 = Category.objects.create(
            name='test cat 2', slug='cat_2')

        self.title = Title.objects.create(
            name='Test Title',
            year='2000',
            description='',
            category=self.category_1,
        )
        self.title.genre.set(self.genres)

        self.review_1 = Review.objects.create(
            title=self.title,
            author=self.user_1,
            text='тестовое ревью',
            score='5'
        )
        self.review_2 = Review.objects.create(
            title=self.title,
            author=self.user_2,
            text='тестовое ревью второго пользователя',
            score='7'
        )

    def test_get(self):
        """Получаем список всех Review."""
        url = reverse('reviews-list', args=(self.title.id,))
        reviews = Review.objects.all()
        response = self.client.get(url)
        serializer_data = ReviewSerializer(reviews, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        """Создание нового Review."""
        self.assertEqual(2, Review.objects.all().count())
        data = {'text': 'Создал ревью', 'score': 7}
        url = reverse('reviews-list', args=(self.title.id,))
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Review.objects.all().count())
        new_review = Review.objects.all().first()
        serializer_data = ReviewSerializer(new_review).data
        self.assertEqual(response.json(), serializer_data)
        self.assertEqual('Создал ревью', new_review.text)
        self.assertEqual(7, new_review.score)

    def test_delete(self):
        """Удалить Review."""
        self.staff_user = User.objects.create(username='test_staff_user',
                                              is_staff=True)

        self.assertEqual(2, Review.objects.all().count())
        url = reverse('reviews-detail',
                      args=(self.title.id, self.review_1.id,))

        self.client.force_login(self.user_staff)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Review.objects.all().count())
