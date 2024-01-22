from django.contrib import admin

from .models import Log
from .settings import settings

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('filename', 'date', 'size')
    ordering = settings.SORT

    class Media:
        css = { 'all': ('admin/css/logfile.css',) }

    # Disable all modifying permissions
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
