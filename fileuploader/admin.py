from django.contrib import admin
from .models import Upload

class UploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'uv', 'year', 'semester', 'exam_t', 'uploader', 
                    'arch_t', 'uploaded_date', 'available', )
    list_filter = ('uv', 'year', 'semester', 'exam_t', 'uploader', 
                    'arch_t', 'uploaded_date', 'available', )
    search_fields = ('id', 'uv', 'year', 'semester')
admin.site.register(Upload, UploadAdmin)
