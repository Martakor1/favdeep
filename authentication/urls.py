from rest_framework.routers import DefaultRouter

from authentication.views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = router.urls
