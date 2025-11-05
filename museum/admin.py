from django.contrib import admin
from museum.models import Artifact, Hall, Curator, Group, Exhibition
# Register your models here.

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']

@admin.register(Curator)
class CuratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hall')

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date']