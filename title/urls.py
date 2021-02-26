from django.urls import include, path
from rest_framework.routers import DefaultRouter

from title.views import (
    CategoriesViewSet,
    CommentsViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitlesViewSet,
)

title_router = DefaultRouter()
title_router.register('titles', TitlesViewSet, basename='titles')
title_router.register('genres', GenresViewSet, basename='genres')
title_router.register('categories', CategoriesViewSet, basename='categories')
title_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
title_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(title_router.urls)),
]
