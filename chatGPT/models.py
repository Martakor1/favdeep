import requests

from django.db import models


class ChadGPT(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name of API")
    API = models.CharField(max_length=300, verbose_name="API")

    def __str__(self):
        return self.name