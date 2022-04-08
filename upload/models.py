from django.db import models

# Create your models here.
class Content(models.Model):

    picture = models.FileField(upload_to='picture')
    