from django.contrib import admin
from codetests.models import Poll, Document, UploadForm

class PollAdmin(admin.ModelAdmin):
    prepopulated_fields = {'question': ('pub_date',)}

class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'docfile': ()}

class UploadFormAdmin(admin.ModelAdmin):
    display_fields = ["sender", "problem_id", "message"]

admin.site.register(Poll, PollAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(UploadForm, UploadFormAdmin)
