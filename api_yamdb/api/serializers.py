from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from datetime import datetime as dt

from reviews.models import (
    Title, Genre, Category, Review, Comment, GenreTitle
)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class WriteTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )
        model = Title

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

    def create(self, validated_data):
        if (
                'category' not in self.initial_data
                or 'genre' not in self.initial_data
        ):
            raise serializers.ValidationError(
                'Required fields missed',
                code=status.HTTP_400_BAD_REQUEST
            )
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.get_or_create(
                genre=genre,
                title=title
            )
        return title


class ReadTitleSerializer(serializers.ModelSerializer):
    genre = CategorySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return super().validate(data)
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        review = title.reviews.filter(
            title=title,
            author=self.context['request'].user
        ).exists()
        if review:
            raise serializers.ValidationError(
                'Можно оставить только один отзыв'
            )
        return super().validate(data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
