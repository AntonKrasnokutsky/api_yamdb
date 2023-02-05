from rest_framework import serializers
from django.core import validators

from datetime import datetime as dt
from re import match
from titles.models import (
    Title, Genre, Category, Review, Comment
)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        rep = super(TitleSerializer, self).to_representation(instance)
        rep['category'] = instance.category.slug
        return rep

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


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
