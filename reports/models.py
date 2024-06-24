# from django.db import models
#
# # Create your models here.
# class AWB(models.Model):
#     awb_number = models.IntegerField(primary_key=True)
#     origin = models.CharField(max_length=20)
#     destination = models.CharField(max_length=20)
#     pieces_received = models.PositiveIntegerField()
#     weight_received = models.PositiveIntegerField()
#     weight_on_hand = models.PositiveIntegerField()
#     pieces_on_hand = models.PositiveIntegerField()
#     consignee = models.CharField(max_length=50)
#     description = models.CharField(max_length=250)
#     hours_remaining = models.IntegerField()
#     priority = models.PositiveIntegerField()
#     days = models.PositiveIntegerField()
#     station = models.CharField(max_length=6)
#     remarks = models.CharField(max_length=50, blank=True, null=True)
#     sla_report = models.BooleanField(default=False)
#     top_20_report = models.BooleanField(default=False)
#     priority_report = models.BooleanField(default=False)
#     sent_awb = models.BooleanField(default=False)
#     new_awb = models.BooleanField(default=False)
#     partial_sent_awb = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.awb_number)



from django.db import models

class AWB(models.Model):
    awb_number = models.IntegerField(primary_key=True)
    origin = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    pieces_received = models.PositiveIntegerField()
    weight_received = models.PositiveIntegerField()
    consignee = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    days = models.PositiveIntegerField()
    station = models.CharField(max_length=6)
    sla_report = models.BooleanField(default=False)
    top_20_report = models.BooleanField(default=False)
    main_priority_report = models.BooleanField(default=False)
    sub_priority_report = models.BooleanField(default=False)
    sent_awb = models.BooleanField(default=False)
    new_awb = models.BooleanField(default=False)
    partial_sent_awb = models.BooleanField(default=False)

    def __str__(self):
        return str(self.awb_number)

class SLA(models.Model):
    awb_number = models.IntegerField(AWB, related_name='sla_reports')
    weight_on_hand = models.PositiveIntegerField()
    pieces_on_hand = models.PositiveIntegerField()
    hours_remaining = models.IntegerField()
    priority = models.PositiveIntegerField()

class Waybills(models.Model):
    awb_number = models.IntegerField(AWB, related_name='waybill_reports')
    weight_on_hand = models.PositiveIntegerField()
    pieces_on_hand = models.PositiveIntegerField()
    hours_remaining = models.IntegerField()
    priority = models.PositiveIntegerField()
