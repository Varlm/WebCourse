from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from museum.api import (
    ArtifactsViewset, HallsViewset, CuratorsViewset,
    GroupsViewset, ExhibitionsViewset, UserProfileViewset
)
from django.conf import settings
from django.conf.urls.static import static
from museum.views import RegisterView


router = DefaultRouter()
router.register('users', UserProfileViewset, basename='users')
router.register("museum", ArtifactsViewset, basename="museum")
router.register("halls", HallsViewset, basename="halls")
router.register("curators", CuratorsViewset, basename="curators")
router.register("groups", GroupsViewset, basename="groups")
router.register("exhibitions", ExhibitionsViewset, basename="exhibitions")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', lambda request: HttpResponse("Django сервер работает!")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
