from django.contrib import admin

from jsonfield import JSONField
from jsoneditor.forms import JSONEditor

from .models import DjangoRestClient


class DjangoRestClientAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'config': JSONEditor},
    }


admin.site.register(DjangoRestClient)
