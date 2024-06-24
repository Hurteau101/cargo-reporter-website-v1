from .models import AWB
from django.db import transaction


@transaction.atomic
def sla_top_20_save(report_data):
    if AWB.objects.filter(sla_report=True, top_20_report=True).exists():
        AWB.objects.filter(sla_report=True, top_20_report=True).delete()

    awb_objects_to_create = []
    batch_size = 100

    for data in report_data:
        for awb_details in data["awb_details"]:
            awb_obj = AWB(
                awb_number=awb_details["awb"],
                origin="WPG",
                destination=data["destination"],
                pieces_received=awb_details["piece_rcd"],
                weight_received=awb_details["weight_rcd"],
                weight_on_hand=awb_details["weight_on_hand"],
                pieces_on_hand=awb_details["piece_count_on_hand"],
                consignee=awb_details["consignee"],
                description=awb_details["goods_desc"],
                hours_remaining=awb_details["hours_remaining"],
                priority=awb_details["priority"],
                days=awb_details["days_on_hand"],
                station="WPG",
                sla_report=True,
                top_20_report=True,
            )

            awb_objects_to_create.append(awb_obj)

            if len(awb_objects_to_create) >= batch_size:
                AWB.objects.bulk_create(awb_objects_to_create)
                awb_objects_to_create = []

    if awb_objects_to_create:
        with transaction.atomic():
            AWB.objects.bulk_create(awb_objects_to_create)


def priority_save(report_data):
    # not = Makes it True if no report found
    priority_report = not AWB.objects.filter(priority_report=True).exists()

    new_awb_pieces_dict = {}
    new_awb_weight_dict = {}

    for data in report_data:
        for awb_details in data["awb_details"]:
            if not priority_report:
                new_awb_pieces_dict.update({int(awb_details["awb"]): awb_details["piece_count_on_hand"]})
                new_awb_weight_dict.update({int(awb_details["awb"]): awb_details["weight_on_hand"]})

            awb, created = AWB.objects.get_or_create(
                awb_number=data["awb"],
                defaults={
                    "awb_number" : awb_details["awb"],
                    "origin": "WPG",
                    "destination": data["destination"],
                    "pieces_received": awb_details["piece_rcd"],
                    "weight_received": awb_details["weight_rcd"],
                    "weight_on_hand": awb_details["weight_on_hand"],
                    "pieces_on_hand": awb_details["piece_count_on_hand"],
                    "consignee": awb_details["consignee"],
                    "description": awb_details["goods_desc"],
                    "hours_remaining": awb_details["hours_remaining"],
                    "priority": awb_details["priority"],
                    "days": awb_details["days_on_hand"],
                    "station": "WPG",
                    "sla_report": True,
                    "top_20_report": True,
                }
            )