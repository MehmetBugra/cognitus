from django.db import models


class DataModel(models.Model):
    class Meta:
        verbose_name = 'Data'
        verbose_name_plural = 'Datas'

    text = models.TextField()
    label = models.TextField()
