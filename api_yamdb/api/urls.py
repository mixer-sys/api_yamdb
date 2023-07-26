from django.urls import path, include

from rest_framework.routers import SimpleRouter
from users.views import UserViewSet
# from reviews.views import ...


router_api_v1 = SimpleRouter()

router_api_v1.register(r'users', UserViewSet, basename='user')
# router_api_v1.register('reviews', ReviewsViewset, basename='groups')
# ...

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
