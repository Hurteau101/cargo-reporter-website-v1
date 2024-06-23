from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_importer, name='report-importer'),
]