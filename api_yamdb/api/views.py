from rest_framework import (
    viewsets, filters, status, mixins
)
from django_filters.rest_framework import (
    DjangoFilterBackend, FilterSet,
    CharFilter, NumberFilter
)
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from titles.models import Title, Genre, Category, Review, GenreTitle
from .serializers import (
    WriteTitleSerializer, GenreSerializer, CategorySerializer,
    ReviewSerializer, ReadTitleSerializer
)
from .permissions import (
    IsUserOrReadOnly, IsModeratorOrReadOnly,
    IsAdministratorOrReadOnly, IsSuperUserOrReadOnly
)


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TittleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = ReadTitleSerializer
    permission_classes = [IsAdministratorOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return self.serializer_class
        return WriteTitleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = Title.objects.get(id=self.kwargs.get('id'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdministratorOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        instance = Genre.objects.get(slug=self.kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdministratorOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        instance = Category.objects.get(slug=self.kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsUserOrReadOnly, IsModeratorOrReadOnly,
        IsAdministratorOrReadOnly, IsSuperUserOrReadOnly
    )

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        return Review.objects.filter(title=title_id)

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return (только_чтение(),)
    #     return super().get_permissions()

    def perform_create(self, serializer):
        if not serializer.is_valid():
            return super().permission_denied(self.request)
        title = Title.objects.get(pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)

