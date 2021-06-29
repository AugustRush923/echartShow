from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.auth import get_permission_codename
from .models import Data


# Register your models here.

@admin.register(Data)
class DataManagerAdmin(admin.ModelAdmin):
    list_filter = (
        'data_months', 'hscode', 'product_name', 'export_type',
    )
    list_display = (
        'data_months', 'hscode', 'product_name', 'export_data_2019', 'export_data_2020', 'export_data_2021',
        'export_type', 'unit', 'get_all_year_line_chart', 'get_2019_line_chart', 'get_2020_line_chart',
        'get_2021_line_chart',
    )
    search_fields = ('hscode', 'product_name')
    list_per_page = 24
    ordering = ('hscode', 'export_type', 'data_months',)
    fieldsets = (
        (None, {'fields': [('data_months', 'hscode', 'product_name')]}),
        (None, {'fields': [('export_data_2019', 'export_data_2020', 'export_data_2021')]}),
        (None, {'fields': (('export_type', 'unit'),)}),
        (None, {'fields': ('is_delete',)}),
    )
    actions = ("set_status_visible", "set_status_invisible")

    def set_status_visible(self, request, queryset):
        queryset.update(is_delete=True)
        self.message_user(request, "操作成功")

    set_status_visible.short_description = "使所选 可见"
    set_status_visible.allowed_permissions = ['set_visible']

    def has_set_visible_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('set_visible', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def set_status_invisible(self, request, queryset):
        queryset.update(is_delete=False)
        self.message_user(request, "操作成功")

    set_status_invisible.short_description = "使所选 不可见"
    set_status_invisible.allowed_permissions = ['set_invisible']

    def has_set_invisible_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('set_invisible', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def get_all_year_line_chart(self, obj):
        if obj.export_type != "value of exports":
            return mark_safe(
                u'<a href="/show/?hscode=%s" target="_blank">%s</a>' % (
                    obj.hscode, "全年出口量"))
        return mark_safe(
            u'<a href="/show/?hscode=%s&export_type=value of exports" target="_blank">%s</a>' % (
                obj.hscode, "全年出口额"))

    get_all_year_line_chart.short_description = "全年走势图"

    def get_2019_line_chart(self, obj):
        if obj.export_type != "value of exports":
            return mark_safe(u'<a href="/show/%s/2019/" target="_blank">%s</a>' % (obj.hscode, "2019出口量"))
        return mark_safe(
            u'<a href="/show/%s/2019/?export_type=value of exports" target="_blank">%s</a>' % (obj.hscode, "2019出口额"))

    get_2019_line_chart.short_description = "2019年走势图"

    def get_2020_line_chart(self, obj):
        if obj.export_type != "value of exports":
            return mark_safe(u'<a href="/show/%s/2020/" target="_blank">%s</a>' % (obj.hscode, "2020出口量"))
        return mark_safe(
            u'<a href="/show/%s/2020/?export_type=value of exports" target="_blank">%s</a>' % (obj.hscode, "2020出口额"))

    get_2020_line_chart.short_description = "2020年走势图"

    def get_2021_line_chart(self, obj):
        if obj.export_type != "value of exports":
            return mark_safe(u'<a href="/show/%s/2021/" target="_blank">%s</a>' % (obj.hscode, "2021出口量"))
        return mark_safe(
            u'<a href="/show/%s/2021/?export_type=value of exports" target="_blank">%s</a>' % (obj.hscode, "2021出口额"))

    get_2021_line_chart.short_description = "2021年走势图"


admin.site.site_title = "数据展示"
admin.site.site_header = "数据管理"
