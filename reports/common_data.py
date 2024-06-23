from .models import AWB
from django.db.models import Sum

DESTINATION_FILTER_LIST = [
    "YTH", "YST", "YIV", "WGK", "YGO", "YOH", "YRS", "ZGI", "YNE", "YCR", "YBT", "ZTM", "YPM", "XLB", "XTL", "XSI",
    "ZAC", "ZSJ"
]


def get_past_sla_data(destination_filter, station, hours):
    return AWB.objects.filter(sla_report=True, hours_remaining__lt=hours, station=station, destination__in=destination_filter).values(
        'destination').annotate(
        total_weight=Sum('weight_on_hand'))


def get_total_weight(destination_filter, station, hours):
    return AWB.objects.filter(sla_report=True, hours_remaining__lt=hours, station=station, destination__in=destination_filter).values(
        'destination').aggregate(
        total_weight=Sum('weight_on_hand'))['total_weight']
