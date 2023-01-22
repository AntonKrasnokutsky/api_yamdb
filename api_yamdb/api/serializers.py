from rest_framework import serializers

from datetime import datetime as dt
from titles.models import Title, Genre, Category


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

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

