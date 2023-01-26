from django.contrib import admin
from .models import Title, Genre, GenreTitle, Category

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Category)
