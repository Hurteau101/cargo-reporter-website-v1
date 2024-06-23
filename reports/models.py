from django.db import models

# Create your models here.
class AWB(models.Model):
    awb_number = models.IntegerField(primary_key=True)
    origin = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    pieces_received = models.PositiveIntegerField()
    weight_received = models.PositiveIntegerField()
    weight_on_hand = models.PositiveIntegerField()
    pieces_on_hand = models.PositiveIntegerField()
    consignee = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    hours_remaining = models.IntegerField()
    priority = models.PositiveIntegerField()
    days = models.PositiveIntegerField()
    station = models.CharField(max_length=6)
    remarks = models.CharField(max_length=50)
    sla_report = models.BooleanField(default=False)
    top_20_report = models.BooleanField(default=False)
    priority_report = models.BooleanField(default=False)
    sent_awb_indication = models.BooleanField(default=False)
    new_awb_indication = models.BooleanField(default=False)
    partial_indication = models.BooleanField(default=False)

    def __str__(self):
        return str(self.awb_number)


