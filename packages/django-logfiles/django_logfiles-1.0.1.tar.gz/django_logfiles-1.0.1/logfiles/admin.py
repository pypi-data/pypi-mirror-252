from django.contrib import admin

from .models import Log
from .settings import settings

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('filename', 'date', 'size_formatted')
    ordering = settings.SORT

    def size_formatted(self, obj):
        return '{:_}'.format(obj.size).replace('_', ' ')
    size_formatted.admin_order_field = 'size'
    size_formatted.short_description = 'Size'

    class Media:
        css = { 'all': ('admin/css/logfile.css',) }

    # Disable all modifying permissions
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
