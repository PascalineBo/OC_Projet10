from django.contrib import admin

from .models import Project, Issue, Contributor, Comment

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Contributor)
admin.site.register(Comment)

# class ContributorAdmin(admin.ModelAdmin):
    # search_fields = ['user_id', 'project_id', 'permission', 'role']


# Register your models here.
