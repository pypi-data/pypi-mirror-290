from django.contrib import admin
from django.contrib.admin import register

from .models import TropipayOrder


@register(TropipayOrder)
class TropipayOrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'uuid', 'name', 'last_name', 'email', 'total')
    list_display_links = list_display
    list_filter = ('created_at',)
    search_fields = ('uuid', 'title', 'name', 'last_name', 'email', 'phone_number', 'description', 'location')
    fieldsets = [
        ('Main Data', {
            'fields': (
                'uuid', 'created_at', 'total', 'location',
            )
        },),
        ('Personal Info', {
            'fields': (
                ('name', 'last_name'),
                'title',
                ('email', 'phone_number'),
            )
        },),
        ('Other', {
            'fields': ('description',)
        },),
    ]


