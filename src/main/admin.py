from django.contrib import admin
from main import models


@admin.register(models.Document)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author',)
    date_hierarchy = 'created_at'
    search_fields = ('title',)
