from rest_framework import serializers

from datetime import datetime as dt
from re import match
from titles.models import (
    Title, Genre, Category, Review, Comment
)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)

    def validate_slug(self, value):
        if match(r'^[-a-zA-Z0-9_]+$', value) is None:
            raise serializers.ValidationError(
                'Slug format error'
            )
        if not value:
            raise serializers.ValidationError(
                'Slug can not be empty'
            )
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)

    def validate_slug(self, value):
        if match(r'^[-a-zA-Z0-9_]+$', value) is None:
            raise serializers.ValidationError(
                'Slug format error'
            )
        if not value:
            raise serializers.ValidationError(
                'Slug can not be empty'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    # comments = CommentSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',) # comments
