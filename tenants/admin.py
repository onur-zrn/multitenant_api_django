from django.contrib import admin
from .models import Center, Domain

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'schema_name')

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('is_primary',)