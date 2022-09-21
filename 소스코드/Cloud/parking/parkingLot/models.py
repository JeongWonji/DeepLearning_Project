from django.db import models

class Parking(models.Model):
    img = models.CharField(max_length=200, blank=True, null=True)
    car_number = models.CharField(max_length=10, blank=True, null=True)
    handicap = models.CharField(max_length=2, blank=True, null=True)
    enter = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parking'