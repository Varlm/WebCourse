from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from museum.models import Artifact, Hall, Curator, Exhibition, Group
from museum.serializers import ArtifactSerializer, HallSerializer, CuratorSerializer, GroupSerializer, ExhibitionSerializer
class ArtifactsViewset (mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):

    queryset = Artifact.objects.all()
    serializer_class=ArtifactSerializer


class HallsViewset(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

class GroupsViewset(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CuratorsViewset(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer




class ExhibitionsViewset(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    queryset = Exhibition.objects.all()
    serializer_class = ExhibitionSerializer