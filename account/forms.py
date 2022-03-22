from urllib import request
from django import forms 
from django.db.models import Min, Max
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 

from predict.models import History
 

class PdfGenForm(forms.Form):

    fromDate = forms.DateField(required=False)
    toDate = forms.DateField(required=False)

    def clean(self):
        cleaned_data = super().clean() 
        user_toDate = cleaned_data.get('toDate')
        user_fromDate = cleaned_data.get('fromDate')

        print(user_toDate, user_fromDate)

        history_obj = History.objects.values('date_time__date')
        min_date = history_obj.aggregate(Min('date_time__date'))['date_time__date__min']
        max_date = history_obj.aggregate(Max('date_time__date'))['date_time__date__max']

        print(min_date, max_date)

        if user_toDate and user_fromDate:
            if user_fromDate > user_toDate:
                raise ValidationError("'From-date' cannot be greater than 'To-date'")
            
            if user_fromDate: 
                if not(min_date <= user_fromDate <= max_date):
                    raise ValidationError(f"'From-date' is out of range from all search history dates.(date range in database[{min_date} to {max_date}].")

            if user_toDate: 
                if not(min_date <= user_toDate <= max_date):
                    raise ValidationError(f"'To-date' is out of range from all search history dates.(date range in database[{min_date} to {max_date}].")
            
        else: 
            if user_fromDate: 
                if not(min_date <= user_fromDate <= max_date):
                    raise ValidationError(f"'From-date' is out of range from all search history dates.(date range in database[{min_date} to {max_date}].")
                
            if user_toDate: 
                if not(min_date <= user_toDate <= max_date):
                    raise ValidationError(f"'To-date' is out of range from all search history dates.(date range in database[{min_date} to {max_date}].")
            
            
class UserEditForm(forms.ModelForm):

    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].required = True 
