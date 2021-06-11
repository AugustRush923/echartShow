from django.contrib import admin
from .models import Data


# Register your models here.

@admin.register(Data)
class DataManagerAdmin(admin.ModelAdmin):
    list_filter = (
        'data_months', 'hscode', 'product_name', 'export_type',
    )
    list_display = (
        'data_months', 'hscode', 'product_name', 'export_data_2019', 'export_data_2020', 'export_data_2021',
        'export_type', 'unit'
    )
    search_fields = ('hscode', 'product_name')
    list_per_page = 24
    ordering = ('hscode', 'export_type', 'data_months', )
    fieldsets = (
        (None, {'fields': [('data_months', 'hscode', 'product_name')]}),
        (None, {'fields': [('export_data_2019', 'export_data_2020', 'export_data_2021')]}),
        (None, {'fields': (('export_type', 'unit'),)}),
        (None, {'fields': ('is_delete',)}),
    )


admin.site.site_title = "数据展示"
admin.site.site_header = "数据管理"
