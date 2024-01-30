from django.db import models


class ArrestRecord(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    agency = models.CharField(max_length=200)
    severity = models.CharField(max_length=50)
    charge = models.CharField(max_length=200)
    statute = models.CharField(max_length=200)
    arrest_type = models.CharField(max_length=200)
    age = models.IntegerField(null=True, blank=True)
    arrest_date = models.DateField(null=True, blank=True)
    arrest_time = models.TimeField(null=True, blank=True)
    case_number = models.CharField(max_length=200)
    state_lawyer = models.CharField(max_length=200, null=True, blank=True)
    defendant_lawyer = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
