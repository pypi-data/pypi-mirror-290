"""App related API urls."""

from rest_framework import routers

from kalabash.sievefilters.api.v2 import viewsets

router = routers.SimpleRouter()
router.register(r"account/filtersets", viewsets.FilterSetViewSet, basename="filterset")

urlpatterns = router.urls
