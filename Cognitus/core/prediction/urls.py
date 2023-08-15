from django.urls import path
from .views import ( 
    IndexAPIView,
    CreateDataAPIView,
    ReadDatasAPIView,
    UpdateDataAPIView,
    DestroyDataAPIView,
    FileUploadAPIView,
    TrainDataAPIView,
    PredictAPIView,
    ReadLogAPIView
    )

urlpatterns = [
    path('', IndexAPIView.as_view()),
    path("get-data/", ReadDatasAPIView.as_view()),
    path('add-data/', CreateDataAPIView.as_view()),
    path('update-data/<int:id>', UpdateDataAPIView.as_view()),
    path('delete-data/<int:id>', DestroyDataAPIView.as_view()),
    path('upload-file/', FileUploadAPIView.as_view()),
    path('train_data/', TrainDataAPIView.as_view()),
    path('predict/',PredictAPIView.as_view()),
    path('log/',ReadLogAPIView.as_view()),
]
