from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import ArrestRecordResource

# Register your models here.
@admin.register(ArrestRecord)
class ArrestRecordAdmin(ImportExportModelAdmin):
    resource_class = ArrestRecordResource
    list_display = ('name', 'address', 'agency', 'severity', 'charge', 'statute', 'arrest_type', 'age', 'arrest_date', 'arrest_time', 'state_lawyer', 'defendant_lawyer')