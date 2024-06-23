from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_importer, name='report-importer'),
    path('top-20', views.top_20, name='top-20'),
    path('sla', views.sla, name='sla'),
    path('sla/destination-breakdown/<str:destination>', views.destination_breakdown, name='destination-breakdown'),
]