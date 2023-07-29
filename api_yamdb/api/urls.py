from django.urls import path, include
from rest_framework.routers import SimpleRouter
from users.views import (
    UserViewSet, CreateUserView,
    get_token_jwt
)
from api.views import (
    CategoryViewSet, CommentViewSet,
    GenreViewSet, ReviewViewSet,
    TitlesViewSet, ReviewViewSet,
)

app_name = 'api'

router_api_v1 = SimpleRouter()
router_api_v1.register(r'categories', CategoryViewSet)
router_api_v1.register(r'genres', GenreViewSet)
router_api_v1.register(r'titles', TitlesViewSet)
router_api_v1.register(r'users', UserViewSet, basename='user')
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/auth/signup/', CreateUserView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        get_token_jwt,
        name='token_obtain'
    ),
    path('v1/', include(router_api_v1.urls)),
]
