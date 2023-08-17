from django.db import models


class DataModel(models.Model):
    class Meta:
        verbose_name = 'Data'
        verbose_name_plural = 'Datas'

    text = models.TextField()
    label = models.TextField()


class LogModel(models.Model):
    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
    
    message = models.CharField()
    accuracy = models.CharField()
    started_date = models.CharField()
    finished_date = models.CharField()

