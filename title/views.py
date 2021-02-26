from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from title.custom_viewset_models import WithNoDetails
from title.filters import TitleFilter
from title.models import Category, Genre, Review, Title
from title.permissions import IsYAMDBPermission, IsStaffOrReadOnly
from title.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleCreateSerializer,
)

User = get_user_model()


class TitlesViewSet(ModelViewSet):
    """Работа с произведениями."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return TitleCreateSerializer
        return TitleSerializer


class GenresViewSet(WithNoDetails):
    """Работа с жанрами."""
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsStaffOrReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoriesViewSet(WithNoDetails):
    """Работа с категориями."""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsStaffOrReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ReviewViewSet(ModelViewSet):
    """Работа с отзывами."""
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsYAMDBPermission,
                          )
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(
            Title.objects.prefetch_related('reviews').all(),
            id=title_id,
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ModelViewSet):
    """Работа с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsYAMDBPermission,)

    def get_queryset(self, **kwargs):
        """Создаем queryset из комментов одного ревью."""
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(
            Review.objects.prefetch_related('comments').all(),
            id=review_id,
            title=title
        )
        return review.comments.all()

    def perform_create(self, serializer):
        """Создаем комментарий к ревью."""
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review, )
