from django.db.models import Avg
from django_filters.rest_framework import (
    DjangoFilterBackend, FilterSet, CharFilter, NumberFilter,
)
from rest_framework import filters, viewsets
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleCreateSerializer,
    TitleSerializer, ReviewSerializer, CommentSerializer
)
from reviews.models import Category, Genre, Title, Review
from users.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from api.permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug',)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug',)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleFilters(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'name'
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilters
    search_fields = ('name', 'genre', 'category')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        if title.reviews.filter(author=self.request.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.kwargs.get('title_id'))

    def update(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['pk'])
        if review.author != self.request.user:
            user = get_object_or_404(User, username=self.request.user)
            if user.role not in ('moderator', 'admin'):
                return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['pk'])
        if review.author != self.request.user:
            user = get_object_or_404(User, username=self.request.user)
            if user.role not in ('moderator', 'admin'):
                return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        get_object_or_404(Review, id=self.kwargs['review_id'])
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.kwargs.get('review_id'))

    def update(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        comment = get_object_or_404(review.comments, id=self.kwargs['pk'])
        if comment.author != self.request.user:
            user = get_object_or_404(User, username=self.request.user)
            if user.role not in ('moderator', 'admin'):
                return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        comment = get_object_or_404(review.comments, id=self.kwargs['pk'])
        if comment.author != self.request.user:
            user = get_object_or_404(User, username=self.request.user)
            if user.role not in ('moderator', 'admin'):
                return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()
