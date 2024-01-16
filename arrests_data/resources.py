from import_export import resources, fields
from import_export.widgets import DateWidget
from .models import ArrestRecord
from datetime import datetime

class ArrestRecordResource(resources.ModelResource):
    arrest_date = fields.Field(
        attribute='arrest_date',
        column_name='arrest_date',
        widget=DateWidget(format='%a %m/%d'), # Custom date format
    )

    def before_import_row(self, row, **kwargs):
        # Convert the 'arrest_date' field to the correct format
        raw_date = row['arrest_date']
        if raw_date:
            # Assuming the year is missing, append the current year or a default year
            current_year = datetime.now().year
            formatted_date = f"{raw_date} {current_year}"
            # Parse the date
            row['arrest_date'] = datetime.strptime(formatted_date, '%a %m/%d %Y').date()

    class Meta:
        model = ArrestRecord
