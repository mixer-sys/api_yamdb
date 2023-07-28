from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import UserViewSet, CreateUserView
from api.views import CommentViewSet, TitleViewSet, ReviewViewSet


app_name = 'api'

router_api_v1 = SimpleRouter()
router_api_v1.register(r'users', UserViewSet, basename='user')
router_api_v1.register(r'titles', TitleViewSet)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet
)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)


urlpatterns = [
    path('v1/auth/signup/', CreateUserView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('v1/', include(router_api_v1.urls)),
]
