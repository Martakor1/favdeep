from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models
from django.utils import timezone

from authentication.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Адрес электронной почты", db_index=True, unique=True)

    first_name = models.CharField("Имя", max_length=255, blank=False)

    last_name = models.CharField("Фамилия", max_length=255, blank=False)

    patronymic = models.CharField("Отчество", max_length=255, null=True, blank=True)

    # по возможности выделить в отдельную таблицу
    organisation = models.CharField("Наименование организации", max_length=255, null=True, blank=True)

    organisation_sector = models.CharField("Отрасль деятельности", max_length=255, null=True, blank=True)

    inn = models.CharField("ИНН", max_length=25, blank=False)

    weblink = models.URLField("Сайт организации", null=True, blank=False)

    # по возможности выделить в отдельную таблицу
    country = models.CharField("Страна", max_length=128)

    city = models.CharField("Город", max_length=128)

    work_position = models.CharField("Должность", max_length=128, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField("Дата входа", default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = " ".join([str(self.last_name),
                              str(self.first_name),
                              str(self.patronymic)])
        return full_name

    def get_username(self):
        return self.email