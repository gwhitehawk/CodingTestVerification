from django.contrib import admin
from codetests.models import User, Problem, Test

class UserAdmin(admin.ModelAdmin):
    display_fields = ["email", "password"]

class ProblemAdmin(admin.ModelAdmin):
    display_fields = ["title", "statement"]

class TestAdmin(admin.ModelAdmin):
    display_fields = ["problem_title", "test_input", "max_duration"]

admin.site.register(User, UserAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Test, TestAdmin)
