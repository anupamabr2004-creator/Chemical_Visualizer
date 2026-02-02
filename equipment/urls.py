from django.urls import path
from .views import UploadCSV, DatasetList, ExportPDF, DataSummary, DatasetDetail

urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload-csv'),
    path('datasets/', DatasetList.as_view(), name='dataset-list'),
    path('datasets/<int:dataset_id>/', DatasetDetail.as_view(), name='dataset-detail'),
    path('datasets/<int:dataset_id>/export-pdf/', ExportPDF.as_view(), name='export-pdf'),
    path('summary/', DataSummary.as_view(), name='data-summary'),
]
