from __future__ import unicode_literals

from django.db import models

class RealEstate(models.Model):
    district = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
