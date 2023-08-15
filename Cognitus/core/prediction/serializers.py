from rest_framework import serializers
from .models import DataModel
import pandas as pd

class DatasViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataModel
        fields = '__all__'


class CreateDataSerializer(serializers.Serializer):
    label = serializers.CharField()
    text = serializers.CharField()


class DestroyDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class UpdateDataSerializer(serializers.Serializer):
    label = serializers.CharField()
    text = serializers.CharField()


class UploadFileSerializer(serializers.Serializer):
    myFile = serializers.FileField()

    def to_internal_value(self, data):
        return data  # dosya uzantısını vs kontrol edip öyle döndürebilirsin


class PredictSerializer(serializers.Serializer):
    predict_text = serializers.CharField()
