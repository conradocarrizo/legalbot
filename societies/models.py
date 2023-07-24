from django.db import models
from django.contrib.postgres.fields import ArrayField

from utils.validators import rut_validator


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Rut(TimeStampMixin):
    "Esta representa el Rut(Rol Único Tributario) para personas naturales(físicas) y jurídicas"
    code = models.CharField(
        max_length=10, validators=[rut_validator], unique=True, db_index=True
    )
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"[{self.code}] {self.name}"


class Person(TimeStampMixin):
    "Representa Personas físicas"

    rut = models.ForeignKey(Rut, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.rut.name}"


class Society(TimeStampMixin):
    "Representa Personas jurídicas"

    rut = models.ForeignKey(Rut, on_delete=models.CASCADE)
    actions = models.PositiveIntegerField(default=0)
    members = models.ManyToManyField(
        Person, through="SocietyMember", related_name="member_society"
    )
    admins = models.ManyToManyField(
        Person, through="SocietyAdmin", related_name="admin_society"
    )

    class Meta:
        verbose_name_plural = "societies"

    def __str__(self):
        return f"[{self.rut.code}] {self.rut.name}"


class SocietyMember(TimeStampMixin):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    member = models.ForeignKey(Person, on_delete=models.CASCADE)
    actions = models.PositiveIntegerField(default=0)

    @property
    def participation(self):
        if self.society.actions:
            return round((self.actions / self.society.actions), 2)


class SocietyAdmin(TimeStampMixin):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    admin = models.ForeignKey(Person, on_delete=models.CASCADE)
    faculties = ArrayField(models.CharField(max_length=50))
