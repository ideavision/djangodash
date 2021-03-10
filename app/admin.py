from django.contrib import admin
from .models import PlotlyDashApp, Company
from .forms import PlotlyDashAppAdmin

admin.site.register(PlotlyDashApp, PlotlyDashAppAdmin)
# admin.site.register(Company)