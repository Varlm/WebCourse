from rest_framework import serializers
from museum.models import Artifact, Group, Hall, Curator, Exhibition
from django.contrib.auth.models import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class ArtifactSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        source='group',
        queryset=Group.objects.all(),
        write_only=True
    )

    class Meta:
        model = Artifact
        fields = ['id', 'name', 'group', 'group_id',"picture"]


class HallSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        source='group',
        queryset=Group.objects.all(),
        write_only=True
    )

    class Meta:
        model = Hall
        fields = ['id', 'name', 'group', 'group_id']


class CuratorSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        source='hall',
        queryset=Hall.objects.all(),
        write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Curator
        fields = ['id', 'user', 'hall', 'hall_id']


class ExhibitionSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        source='hall',
        queryset=Hall.objects.all(),
        write_only=True
    )

    class Meta:
        model = Exhibition
        fields = ['id', 'title', 'date', 'hall', 'hall_id']
