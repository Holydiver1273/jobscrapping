from django import forms
from .models import JobListing 

class JobSearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100, required=False)
    
class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'company', 'location', 'salary', 'description']