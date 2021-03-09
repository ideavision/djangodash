from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from common.dash_validator import DashValidator
from django.core.files import File
from .models import PlotlyDashApp
from guardian.admin import GuardedModelAdmin

class PlotlyDashAppForm(forms.ModelForm):
    creator = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="(Nothing)",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Title",                
                "class": "form-control"
            }
        ))
    dash_file = forms.FileField(
        widget=forms.FileInput(
            attrs={           
                "class": "custom-file-input"
            }
        ))

    class Meta:
        model = PlotlyDashApp
        fields = ('title', 'creator', 'dash_file')

    def clean_dash_file(self):
        dash_file = self.cleaned_data['dash_file']

        ext = self.cleaned_data['dash_file'].name.split('.')[-1]
        if ext != 'py':
            # TODO It's better to check mimetype using first chunk of the file
            raise forms.ValidationError("Dash should be a python file")

        validatior = DashValidator(dash_file)

        if not validatior.has_app_module():
            raise forms.ValidationError("Invalid Dash File")

        if not validatior.is_executeable():
            raise forms.ValidationError("Dash File Is Not Executable")

        return dash_file

    def save(self, commit=True):
        obj = super(PlotlyDashAppForm, self).save(commit=False)
        obj.dash_orginal_name = self.cleaned_data['dash_file'].name
        obj.save()
        return obj

class PlotlyDashAppAdmin(GuardedModelAdmin):
    list_display = ('unique_id', 'title', 'creator', 'dash_orginal_name', 'dash_file')
    form = PlotlyDashAppForm


    