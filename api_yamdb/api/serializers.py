from rest_framework import serializers
from django.core import validators

from datetime import datetime as dt
from re import match
from titles.models import (
    Title, Genre, Category, Review, Comment
)


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        validators=[
            validators.MaxLengthValidator(limit_value=256),
        ]
    )

    class Meta:
        model = Genre
        fields = '__all__'

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        required=True,
        validators=[
            validators.MaxLengthValidator(limit_value=50),
            validators.RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')
        ]
    )

    class Meta:
        model = Category
        fields = '__all__'


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
