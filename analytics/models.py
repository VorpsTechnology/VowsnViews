from django.db import models
from ckeditor.fields import RichTextField


class SendMail(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField()

