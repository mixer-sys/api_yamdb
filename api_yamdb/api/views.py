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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role not in ('admin',):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role not in ('admin',):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role not in ('admin',):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role in ('admin',):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role not in ('admin',):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role in ('admin',):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if user.role in ('user', 'moderator'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role not in ('admin',):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class TitleFilters(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = '__all__'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'name'
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        return (
            TitleCreateSerializer
            if self.request.method
            in (
                'POST',
                'PUT',
                'PATCH',
            )
            else TitleSerializer
        )

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role not in ('admin',):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role not in ('admin',):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.role not in ('admin',):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


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
