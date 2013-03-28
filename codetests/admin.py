from django.contrib import admin
from codetests.models import Document, UploadForm

class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'docfile': ()}

class UploadFormAdmin(admin.ModelAdmin):
    display_fields = ["sender", "problem_id", "message"]

admin.site.register(Document, DocumentAdmin)
admin.site.register(UploadForm, UploadFormAdmin)
