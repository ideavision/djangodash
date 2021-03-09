import os

from django.db import models
from django.core.files import File
from django.contrib.auth.models import User, Group
from common.utils import generate_random_string
from common.dash_validator import DashValidator

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    random_name = generate_random_string()
    filename = "%s.%s" % (random_name, ext)
    return os.path.join('dash_apps/', filename)

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Group.objects.create(name=self.name)
    
class PlotlyDashApp(models.Model):
    unique_id = models.CharField(default=generate_random_string, editable=False, unique=True, max_length=16)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    dash_file = models.FileField(upload_to=get_file_path)
    title = models.CharField(max_length=200)
    dash_orginal_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)   

    @property
    def app_name(self):
        return os.path.basename(self.dash_file.name).split('.')[0]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        validator = DashValidator(self.dash_file)
        new_name = os.path.basename(self.dash_file.name).split('.')[0]
        validator.validate_dash(new_name)

        
