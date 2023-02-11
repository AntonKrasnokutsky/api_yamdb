from rest_framework import serializers, status
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime as dt
from re import match
from titles.models import (
    Title, Genre, Category, Review, Comment, GenreTitle
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


class TitleGenreSerializer(GenreSerializer):

    def to_internal_value(self, data):
        try:
            return GenreSerializer(Genre.objects.get(slug=data)).data
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Жанр со slug "{data}" отсутствует',
                code=status.HTTP_400_BAD_REQUEST
            )


class TitleCategorySerializer(CategorySerializer):
    def to_internal_value(self, data):
        try:
            return CategorySerializer(
                Category.objects.get(
                    slug=data[0] if isinstance(data,list) else data
                )
            ).data
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                f'Категория со slug "{data}" отсутствует',
                code=status.HTTP_400_BAD_REQUEST
            )


class TitleSerializer(serializers.ModelSerializer):
    genre = TitleGenreSerializer(many=True)
    category = TitleCategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        model = Title

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

    def get_rating(self, obj):
        try:
            rating = Review.objects.filter(title=obj).aggregate(
                Avg('score')
            )['score__avg']
        except TypeError:
            rating = None
        return rating

    def create(self, validated_data):
        if ('category' not in self.initial_data
                or 'genre' not in self.initial_data):
            raise serializers.ValidationError(
                'Required fields missed',
                code=status.HTTP_400_BAD_REQUEST
            )
        genres = validated_data.pop('genre')
        validated_data['category'] = Category.objects.get(
            slug=validated_data['category']['slug']
        )
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.get_or_create(
                genre=Genre.objects.get(slug=genre['slug']),
                title=title
            )
        return title

    def update(self, instance, validated_data):
        genres = validated_data.pop('genre')
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)
        instance.category = Category.objects.get(slug=validated_data['category']['slug'])
        GenreTitle.objects.filter(title=instance).delete()
        for genre in genres:
            GenreTitle.objects.create(
                title=instance,
                genre=Genre.objects.get(slug=genre['slug'])
            )
        instance.save()
        return instance


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
