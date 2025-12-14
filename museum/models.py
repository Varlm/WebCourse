from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Group(models.Model):
    name = models.TextField()

    class Meta:
        verbose_name = "Эпоха"
        verbose_name_plural = "Эпохи"
        ordering = ["id"]

    def __str__(self):
        return self.name

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True

class Artifact(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(null=True, upload_to="museum")

    class Meta:
        verbose_name = "Артефакт"
        verbose_name_plural = "Артефакты"

    def __str__(self):
        return self.name

class Hall(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(upload_to='halls/', null=True, blank=True)

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"

    def __str__(self):
        return self.name

class Curator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Куратор"
        verbose_name_plural = "Кураторы"

    def __str__(self):
        return self.user.username

class Exhibition(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    date = models.DateField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Выставка"
        verbose_name_plural = "Выставки"

    def __str__(self):
        return self.title



class UserProfile(TimestampModel):
    class Type(models.TextChoices):
        CURATOR = 'curator', 'Смотритель'
        GUIDE = 'guide', 'Экскурсовод'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(null=True, blank=True)
    stage = models.TextField(null=True, blank=True)
    type = models.TextField(choices=Type.choices, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_type_display()})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
