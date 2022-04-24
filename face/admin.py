from django.contrib import admin
from .models import *
# Register your models here.

from django.db.models import ExpressionWrapper,DateField,Q,F,ManyToOneRel, ForeignKey, OneToOneField , ManyToManyRel, ManyToManyField, AutoField
from django.apps import apps
excluding_list_display = ('created_at','updated_at','is_active','deleted_at')
excluding_fields = ('created_at','updated_at','is_active','deleted_at', 'paid_at')

models = apps.get_app_config('face').get_models()

for model in models:
    # continue
    try:
        class CustomModelAdmin(admin.ModelAdmin):
            fields = [field.name for field in model._meta.get_fields() if not isinstance(field, (ManyToOneRel,ManyToManyRel,AutoField)) and field.name not in excluding_fields ]
            list_display = [field.name for field in model._meta.get_fields() if not isinstance(field, (ManyToOneRel,ManyToManyRel,ManyToManyField,AutoField)) and field.name not in excluding_list_display ]\
                +  ['id']
            # formfield_overrides = {
            #     Models.JSONField: {'widget': JSONEditorWidget},
            # }
            # list_filter = [field.name for field in model._meta.get_fields() if isinstance(field, (ManyToManyField,ForeignKey)) or field.name in ['length_passing_timespan','length_fee_timespan','is_active']]
        
        admin.site.register(model,CustomModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass
    except:
        admin.site.register(model)


# admin.site.register(Person)
# admin.site.register(Attendance)