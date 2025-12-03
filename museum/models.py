from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Эпоха"
        verbose_name_plural = "Эпохи"

    def __str__(self):
        return self.name


class Artifact(models.Model):
    name = models.TextField("Название")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="museum")
    class Meta:
        verbose_name = "Артефакт"
        verbose_name_plural = "Артефакты"


class Hall(models.Model):
    name = models.TextField("Название")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    picture = models.ImageField(upload_to='halls/', null=True, blank=True)
    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"


class Curator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Куратор"
        verbose_name_plural = "Кураторы"

    def __str__(self):
        return self.user.username


class Exhibition(models.Model):
    title = models.TextField("Название выставки")
    date = models.DateField("Дата проведения")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Выставка"
        verbose_name_plural = "Выставки"

    def __str__(self):
        return self.title
