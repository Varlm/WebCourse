import pytest
from datetime import date
from rest_framework.test import APIClient
from django.test import TestCase
from model_bakery import baker
from museum.models import Artifact, Group, Hall, Curator, Exhibition
from django.contrib.auth.models import User

@pytest.mark.django_db
class ArtifactAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        grp = baker.make("museum.Group")
        artifact = baker.make("museum.Artifact", group=grp)

        response = self.client.get('/api/museum/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['id'] == artifact.id
        assert data[0]['name'] == artifact.name
        assert data[0]['group']['id'] == grp.id
        assert data[0]['group']['name'] == grp.name

    def test_create_artifact(self):
        grp = baker.make("museum.Group")
        response = self.client.post("/api/museum/", {
            "name": "Артифакт",
            "group_id": grp.id
        }, format='json')
        assert response.status_code == 201
        data = response.json()
        new_artifact = Artifact.objects.get(id=data['id'])
        assert new_artifact.name == "Артифакт"
        assert new_artifact.group == grp

    def test_delete_artifact(self):
        artifacts = baker.make("museum.Artifact", 3, group=baker.make("museum.Group"))
        artifact_id = artifacts[1].id
        response = self.client.delete(f'/api/museum/{artifact_id}/')
        assert response.status_code == 204
        assert not Artifact.objects.filter(id=artifact_id).exists()

    def test_update_artifact(self):
        artifact = baker.make("museum.Artifact", group=baker.make("museum.Group"))
        response = self.client.patch(f'/api/museum/{artifact.id}/', {"name": "Новое имя"}, format='json')
        assert response.status_code == 200
        artifact.refresh_from_db()
        assert artifact.name == "Новое имя"


@pytest.mark.django_db
class GroupAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        group = baker.make("museum.Group", name="Эпоха Возрождения")
        response = self.client.get('/api/groups/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['name'] == "Эпоха Возрождения"
        assert data[0]['id'] == group.id

    def test_create_group(self):
        response = self.client.post("/api/groups/", {"name": "Античность"}, format='json')
        assert response.status_code == 201
        data = response.json()
        assert data['name'] == "Античность"
        assert Group.objects.filter(name="Античность").exists()

    def test_delete_group(self):
        groups = baker.make("museum.Group", 2)
        group_id = groups[0].id
        response = self.client.delete(f'/api/groups/{group_id}/')
        assert response.status_code == 204
        assert not Group.objects.filter(id=group_id).exists()

    def test_update_group(self):
        group = baker.make("museum.Group", name="Старое имя")
        response = self.client.patch(f'/api/groups/{group.id}/', {"name": "Новое имя"}, format='json')
        assert response.status_code == 200
        group.refresh_from_db()
        assert group.name == "Новое имя"

# ---------------- Hall ----------------
@pytest.mark.django_db
class HallAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        group = baker.make("museum.Group")
        hall = baker.make("museum.Hall", name="Зал античности", group=group)
        response = self.client.get('/api/halls/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['name'] == "Зал античности"
        assert data[0]['group']['id'] == group.id

    def test_create_hall(self):
        group = baker.make("museum.Group")
        response = self.client.post("/api/halls/", {"name": "Новый зал", "group_id": group.id}, format='json')
        assert response.status_code == 201
        hall = Hall.objects.get(id=response.json()['id'])
        assert hall.name == "Новый зал"
        assert hall.group == group

    def test_delete_hall(self):
        halls = baker.make("museum.Hall", 2, group=baker.make("museum.Group"))
        hall_id = halls[0].id
        response = self.client.delete(f'/api/halls/{hall_id}/')
        assert response.status_code == 204
        assert not Hall.objects.filter(id=hall_id).exists()

    def test_update_hall(self):
        hall = baker.make("museum.Hall", name="Старый зал", group=baker.make("museum.Group"))
        new_group = baker.make("museum.Group")
        response = self.client.patch(f'/api/halls/{hall.id}/', {"name": "Обновленный зал", "group_id": new_group.id}, format='json')
        assert response.status_code == 200
        hall.refresh_from_db()
        assert hall.name == "Обновленный зал"
        assert hall.group == new_group

@pytest.mark.django_db
class CuratorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        hall = baker.make("museum.Hall")
        user = User.objects.create_user(username="anna", password="12345", first_name="Анна", last_name="Иванова")
        curator = baker.make("museum.Curator", user=user, hall=hall)
        
        response = self.client.get('/api/curators/')
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 1
        
        assert data[0]['user'] == user.id
        assert data[0]['hall']['id'] == hall.id

    def test_create_curator(self):
        hall = baker.make("museum.Hall")
        user = User.objects.create_user(username="petr", password="12345", first_name="Петр", last_name="Сидоров")

        response = self.client.post("/api/curators/", {
            "user": user.id,
            "hall_id": hall.id
        }, format='json')

        assert response.status_code == 201
        curator = Curator.objects.get(id=response.json()['id'])
        assert curator.user == user
        assert curator.hall == hall
    def test_delete_curator(self):
        curators = baker.make("museum.Curator", 2, hall=baker.make("museum.Hall"))
        curator_id = curators[0].id
        response = self.client.delete(f'/api/curators/{curator_id}/')
        assert response.status_code == 204
        assert not Curator.objects.filter(id=curator_id).exists()

    def test_update_curator(self):
        old_hall = baker.make("museum.Hall")
        new_hall = baker.make("museum.Hall")
        user = User.objects.create_user(username="ivan", password="12345", first_name="Иван", last_name="Петров")
        curator = baker.make("museum.Curator", user=user, hall=old_hall)

        response = self.client.patch(f'/api/curators/{curator.id}/', {
            "hall_id": new_hall.id
        }, format='json')

        assert response.status_code == 200

        curator.refresh_from_db()
        assert curator.hall == new_hall
        assert curator.user == user

# ---------------- Exhibition ----------------
@pytest.mark.django_db
class ExhibitionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        exhibition = baker.make("museum.Exhibition", title="Выставка современного искусства", date=date(2024,1,15))
        response = self.client.get('/api/exhibitions/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['title'] == "Выставка современного искусства"
        assert data[0]['date'] == "2024-01-15"

    def test_create_exhibition(self):
        hall = baker.make("museum.Hall")
        response = self.client.post("/api/exhibitions/", {
            "title": "Новая выставка",
            "date": "2024-03-20",
            "hall_id": hall.id
        }, format='json')
    
        assert response.status_code == 201
        data = response.json()
        assert data['title'] == "Новая выставка"
        assert data['hall']['id'] == hall.id

    def test_delete_exhibition(self):
        exhibitions = baker.make("museum.Exhibition", 2)
        exhibition_id = exhibitions[0].id
        response = self.client.delete(f'/api/exhibitions/{exhibition_id}/')
        assert response.status_code == 204
        assert not Exhibition.objects.filter(id=exhibition_id).exists()

    def test_update_exhibition(self):
        exhibition = baker.make("museum.Exhibition", title="Старая выставка", date=date(2024,1,1))
        response = self.client.patch(f'/api/exhibitions/{exhibition.id}/', {"title": "Обновленная выставка", "date": "2024-12-31"}, format='json')
        assert response.status_code == 200
        exhibition.refresh_from_db()
        assert exhibition.title == "Обновленная выставка"
        assert str(exhibition.date) == "2024-12-31"
