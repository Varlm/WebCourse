from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from .models import Artifact, Hall, Curator, Exhibition, Group
from .serializers import (
    ArtifactSerializer, HallSerializer, CuratorSerializer,
    ExhibitionSerializer, GroupSerializer, UserSerializer,
    RegisterSerializer
)
from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet

class UserObjectPermissionMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.is_superuser:
            return qs
        return qs.filter(user=user)

class OwnerProtectionMixin:
    def perform_update(self, serializer):
        obj = self.get_object()
        if not self.request.user.is_superuser and getattr(obj, 'user', None) != self.request.user:
            raise PermissionDenied("Вы не можете изменять чужие объекты")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and getattr(instance, 'user', None) != self.request.user:
            raise PermissionDenied("Вы не можете удалять чужие объекты")
        instance.delete()

class ArtifactsViewset(UserObjectPermissionMixin, OwnerProtectionMixin,
                       mixins.CreateModelMixin, mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        
        # фильтруем по текущему юзеру
        qs = qs.filter(user=self.request.user)

        return qs

class HallsViewset(UserObjectPermissionMixin, OwnerProtectionMixin,
                   mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

class ExhibitionsViewset(UserObjectPermissionMixin, OwnerProtectionMixin,
                         mixins.CreateModelMixin, mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin, mixins.ListModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Exhibition.objects.all()
    serializer_class = ExhibitionSerializer

class GroupsViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CuratorsViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializer
@permission_classes([AllowAny])
class UserProfileViewset(GenericViewSet):
   #queryset=UserProfile.objects.all()
   @action(url_path="my",methods=["GET"], detail=False)
   def get_my(self, request, *args, **kwargs):
       return Response({
           'username': self.request.user.username,
           'is_authenticated':self.request.user.is_authenticated,
            'is_staff':self.request.user.is_staff
       })
   @action(url_path="login",methods=["POST"],detail=False)
   def process_login(self,*args,**kwargs):
       class LoginSerializer(serializers.Serializer):
           username=serializers.CharField()
           password=serializers.CharField()

       serializer=LoginSerializer(data=self.request.data)
       serializer.is_valid(raise_exception=True)
       username=serializer.validated_data['username'] 
       password=serializer.validated_data['password']

       user=authenticate(username=username,password=password)
       if user:
           login(self.request,user)
       else:
           return Response({
               "status":"failed"
           },status=401)
    
       return Response({
           "status": "success"
       })
   @action(url_path="logout",methods=["POST"],detail=False)
   def process_logout(self,*args,**kwargs):
       logout(self.request)   
       return Response({
           "status": "success"
       })
   