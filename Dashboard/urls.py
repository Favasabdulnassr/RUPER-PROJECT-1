from django.urls import path
from.import views

urlpatterns = [
   
path('dashboard/',views.Dashboard,name='dashboard'),
path('download_exel',views.excel_report,name="download_exel"),
path('pdf_download',views.DownloadPDF.as_view(),name='pdf_download'),
]
