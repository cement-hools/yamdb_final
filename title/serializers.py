from rest_framework import serializers
from rest_framework import status
from rest_framework.serializers import ModelSerializer

from title.models import Comment, Review, Title, Genre, Category


class GenreSerializer(ModelSerializer):
    """Сериалайзер Жанры."""

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(ModelSerializer):
    """Сериалайзер Категории."""

    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializer(ModelSerializer):
    """Сериалайзер Произведения."""

    class Meta:
        model = Title
        fields = '__all__'

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=0)


class TitleCreateSerializer(ModelSerializer):
    """Сериалайзер создания и редактирования Произведения."""

    class Meta:
        model = Title
        fields = '__all__'

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )


class ReviewSerializer(ModelSerializer):
    """Сериалайзер Отзывы."""

    class Meta:
        model = Review
        exclude = ('title',)

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    def validate(self, data):
        """У автора только один обзор к Title."""
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs['title_id']
            author = self.context['request'].user
            review_exists = Review.objects.filter(
                author=author,
                title=title_id).exists()
            if review_exists:
                code_400 = status.HTTP_400_BAD_REQUEST
                raise serializers.ValidationError(code=code_400)
        return data


class CommentSerializer(ModelSerializer):
    """Сериалайзер Комментарий."""

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('pub_date',)

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
