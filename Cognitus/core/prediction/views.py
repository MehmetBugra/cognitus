from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView, View
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

import requests
import json

from .serializers import (
    CreateDataSerializer,
    DatasViewSerializer,
    UpdateDataSerializer,
    DestroyDataSerializer,
    UploadFileSerializer,
    PredictSerializer
)


fast_url = "http://algorithm:8001/"

class IndexAPIView(View):  
    def get(self, request):
        return render(request, 'index.html')

class CreateDataAPIView(APIView):
    serializer_class = CreateDataSerializer

    def get(self, request):
        return render(request, 'add-data.html')

    def post(self, request):
        data = json.load(request)

        if 'payload' in data:
            result = data.get('payload')
            serializer = self.serializer_class(data=result)
            serializer.is_valid(raise_exception=True)
            response = requests.post(fast_url + 'create_data', json=serializer.validated_data)
            
            return Response({'status': 'added'}, status=response.status_code)
        
        else:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class ReadDatasAPIView(ListAPIView):
    serializer_class = DatasViewSerializer

    def get(self, request):
        response = requests.get(fast_url + 'get_datas')
        return render(request, 'get-data.html', {'database': response.json()})


class DestroyDataAPIView(APIView):
    serializer_class = DestroyDataSerializer
    
    def delete(self, request):
        r = json.load(request)

        if 'payload' in r:
            payload = r.get('payload')
            serializer = self.serializer_class(data=payload)
            serializer.is_valid(raise_exception=True)
            response = requests.delete(fast_url + 'delete_data', json=serializer.validated_data)
        return Response({'status': 'deleted'}, status=response.status_code)


class UpdateDataAPIView(APIView):
    serializer_class = UpdateDataSerializer
    def put(self, request, id):
        r = json.load(request)

        if 'payload' in r:
            payload = r.get('payload')
            serializer = self.serializer_class(data=payload)
            serializer.is_valid(raise_exception=True)
            response = requests.put(fast_url + f'update_data?inst_id={id}', json=serializer.validated_data)
            return Response({'status': 'updated'}, status=response.status_code)
                
        else:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class FileUploadAPIView(APIView):
    serializer_class = UploadFileSerializer
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _file = {'file': serializer.validated_data['myFile']}
        response = requests.post(fast_url + 'upload_file', files=(_file))
        return Response({'status': 'ok'}, status=response.status_code)


# Prediction

class TrainDataAPIView(APIView):

    def get(self, request):
        response = requests.get(fast_url + 'train_data/')
        return Response({'status' :response.text}, status=response.status_code)


class PredictAPIView(APIView):
    serializer_class = PredictSerializer

    def post(self, request):

        data = json.load(request)

        if 'payload' in data:
            payload = data.get('payload')
            serializer = self.serializer_class(data=payload)
            serializer.is_valid(raise_exception=True)
            response = requests.post(fast_url + f'predict/', json=serializer.validated_data)
            result = response.json()["prediction_result"]
            return Response({'predict_result': result}, status=response.status_code)


class ReadLogAPIView(APIView):
    def get(self, request):
        response = requests.get(fast_url + 'get_log')
        return render(request, 'log.html', {'logs': response.json()['log']})
