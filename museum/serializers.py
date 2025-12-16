from rest_framework import serializers
from .models import Artifact, Hall, Curator, Exhibition, Group, UserProfile
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
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user          
        return super().create(validated_data)    
    class Meta:
        model = Artifact
        fields = ['id', 'name', 'group', 'group_id', 'picture', 'user']
        read_only_fields = ['user']



class HallSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        source='group',
        queryset=Group.objects.all(),
        write_only=True
    )

    class Meta:
        model = Hall
        fields = ['id', 'name', 'group', 'group_id', 'picture', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CuratorSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        source='hall',
        queryset=Hall.objects.all(),
        write_only=True
    )

    class Meta:
        model = Curator
        fields = ['id', 'user', 'hall', 'hall_id']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_superuser:
            return super().create(validated_data)
        validated_data['user'] = request.user
        return super().create(validated_data)

class ExhibitionSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        source='hall',
        queryset=Hall.objects.all(),
        write_only=True
    )

    class Meta:
        model = Exhibition
        fields = ['id', 'title', 'date', 'hall', 'hall_id', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'name', 'stage', 'type', 'created_at', 'updated_at']


class StatsSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=False)
    avg = serializers.FloatField(required=False)
    min = serializers.FloatField(required=False)
    max = serializers.FloatField(required=False)