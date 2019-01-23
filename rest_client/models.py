# from jsonfield import JSONField

from django.db import models

from jsoneditor.fields.django_jsonfield import JSONField


class DjangoRestClient(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    config = JSONField(default={})

    class Meta:
        db_table = 'django_rest_client'

    def __str__(self, *args, **kwargs):
        return self.name
