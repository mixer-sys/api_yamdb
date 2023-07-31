from django.urls import path, include
from rest_framework.routers import SimpleRouter
from users.views import (
    UserView, UserDetailView, SignUpUserView,
    get_token_jwt, SelfView,
)
from api.views import (
    CategoryViewSet, CommentViewSet,
    GenreViewSet, ReviewViewSet,
    TitleViewSet, ReviewViewSet,
)

app_name = 'api'

router_api_v1 = SimpleRouter()
router_api_v1.register(r'categories', CategoryViewSet)
router_api_v1.register(r'genres', GenreViewSet)
router_api_v1.register(r'titles', TitleViewSet)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/auth/signup/', SignUpUserView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        get_token_jwt,
        name='token_obtain'
    ),
    path('v1/users/', UserView.as_view(), name='users'),
    path('v1/users/me/', SelfView.as_view(), name='me'),
    path(
        'v1/users/<slug:username>/',
        UserDetailView.as_view(),
        name='user_detail'
    ),
    path('v1/', include(router_api_v1.urls)),
]
