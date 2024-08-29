from django import forms
from sites.models import Site


class CreateSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ('url', 'name',)
