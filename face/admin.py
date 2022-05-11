from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import *
# Register your models here.
from rangefilter.filters import DateRangeFilter
from django.db.models import ExpressionWrapper,DateField,Q,F,ManyToOneRel, ForeignKey, OneToOneField , ManyToManyRel, ManyToManyField, AutoField
from django.apps import apps
import datetime

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
        x=1
        for obj in queryset:
            if x==1:
                tt =getattr(obj,"time")
                print(type(getattr(obj,"time")))
                print(tt.date())
                print(tt.time())
                x=0
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

    def export_as_csvAgain(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        field_names = ["Date","Name","Std No","Time In","Time Out"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=Attendance-{datetime.datetime.now().date()}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        table = []
        atten = {}
        for obj in queryset:
            # row = [getattr(obj, field) for field in field_names]
            # table.append(row)
            name = getattr(obj,"name")
            #FIXME see this if you change the name
            time = getattr(obj,"time")
            nametime = name + "--" + str(time.date())
            if nametime not in atten:
                out_time = datetime.time(16,0,0,0)
                if time.time()<datetime.time(16,0,0,0):
                    pass
                elif time.time()<datetime.time(18,0,0,0):
                    out_time = datetime.time(16,0,0,0)
                elif time.time()<datetime.time(20,0,0,0):
                    out_time = datetime.time(20,0,0,0)
                else:
                    out_time = datetime.time(23,0,0,0)
                atten[nametime] = [time.time(),out_time]
            else:
                atten[nametime][1] = time.time()


        res = []
        for nametime in atten:
            namedate = nametime.split("--")
            date = namedate[1] if len(namedate)>1 else ""
            name_stdno = nametime.split("--")[0].split("_")
            name = name_stdno[0]
            std_no = name_stdno[1] if len(name_stdno)>1 else ""
            time_in = atten[nametime][0].strftime("%I:%M%p")
            time_out = atten[nametime][1].strftime("%I:%M%p")
        # field_names = ["Name","Std No","Date","Time In","Time Out"]
            row = [date,name,std_no,time_in,time_out]
            # print(row)
            writer.writerow(row)

        return response

    export_as_csvAgain.short_description = "Format Selected"


class TimingsAdmin(admin.ModelAdmin, ExportCsvMixin):
    fields = ['name', 'time']
    list_display = ['name', 'time']
    actions = ["export_as_csv","export_as_csvAgain"]
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