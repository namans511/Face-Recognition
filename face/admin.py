from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import *
# Register your models here.
from rangefilter.filters import DateRangeFilter
from django.db.models import ExpressionWrapper,DateField,Q,F,ManyToOneRel, ForeignKey, OneToOneField , ManyToManyRel, ManyToManyField, AutoField
from django.apps import apps
excluding_list_display = ('created_at','updated_at','is_active','deleted_at')
excluding_fields = ('created_at','updated_at','is_active','deleted_at', 'paid_at')

models = apps.get_app_config('face').get_models()

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class TimingsAdmin(admin.ModelAdmin, ExportCsvMixin):
    fields = ['name', 'time']
    list_display = ['name', 'time']
    actions = ["export_as_csv"]
    # date_hierarchy  = 'time'
    list_filter = (('time', DateRangeFilter),)
    # def export_as_csv(self, request, queryset):
    #     pass

    # export_as_csv.short_description = "Export Selected"

admin.site.register(Timings, TimingsAdmin)

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