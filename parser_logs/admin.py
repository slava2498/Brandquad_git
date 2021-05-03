from django.contrib import admin
from parser_logs.models import *

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_filter = ('method', 'code')
    search_fields = ('id', 'ip_address', 'date_log', 'method', 'url_request', 'code')