from rest_framework import serializers, status

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


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )


    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        model = Title

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

    def create(self, validated_data):
        if ('category' not in validated_data
                or 'genre' not in validated_data):
            raise serializers.ValidationError(
                'Required fields missed',
                code=status.HTTP_400_BAD_REQUEST
            )
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                GenreTitle.objects.get_or_create(
                    genre=genre, title=title
                )
            return title

    def update(self, instance, validated_data):
        genres = validated_data.pop('genre')
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        GenreTitle.objects.filter(title=instance).delete()
        for genre in genres:
            GenreTitle.objects.create(title=instance, genre=genre)
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
