"""This module set up the admin page of django site.
"""
from django.contrib import admin

from .models import Profile,Social_Network_Service,Icon_Mater,Acknowledgment
from .models import Language_Skill, Library_Skill, DevOps_Skill
from .models import Work, Work_Detail
from .models import Work_Language_Skill_RelationShip
from .models import Work_Library_Skill_Relationship
from .models import Work_DevOps_Skill_Relationship

class SNSInline(admin.TabularInline):
    """An inline input form for SNS.
    """
    model = Social_Network_Service
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    """The setting of Profile.
    """
    fieldsets = [
        (None,               {'fields': ['title', 'subtitle']}),
        ('Your information', {'fields': ['last_name', 'first_name', 'job', 'introduction']}),
        ('Photos', {'fields': ['face_photo', 'sub_photo'], 'classes': ['collapse']}),
    ]
    inlines = [SNSInline]
    list_display = ('title', 'last_name', 'first_name')

class WorkDetailInline(admin.TabularInline):
    """An inline input form for work details.
    """
    model = Work_Detail
    extra = 1

class WorkLanguageSkillRelationShipInline(admin.TabularInline):
    """An inline input form for language skills.
    """
    model = Work_Language_Skill_RelationShip
    extra = 3
    ordering = ("sort",)

class WorkLibrarySkillRelationshipInline(admin.TabularInline):
    """An inline input form fofr library skills.
    """
    model = Work_Library_Skill_Relationship
    extra = 3
    ordering = ("sort",)

class WorkDevOpsSkillRelationshipInline(admin.TabularInline):
    """An inline input form for DevOps skills.
    """
    model = Work_DevOps_Skill_Relationship
    extra = 3
    ordering = ("sort",)

class WorkAdmin(admin.ModelAdmin):
    """The setting of works.
    """
    fieldsets = [
        (None,               {'fields': ['title', 'description']}),
        ('URL information', {'fields': ['url' ,'repository_url']}),
        ('Image', {'fields': ['image']}),
        ('other', {'fields': ['private', 'sort']}),
    ]
    inlines = [WorkDetailInline, WorkLanguageSkillRelationShipInline, \
                WorkLibrarySkillRelationshipInline, WorkDevOpsSkillRelationshipInline]
    list_display = ('title', 'private')
    list_filter = ['private']
    search_fields = ['question_text']
    ordering = ("sort",)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Icon_Mater)
admin.site.register(Acknowledgment)
admin.site.register(Language_Skill)
admin.site.register(Library_Skill)
admin.site.register(DevOps_Skill)
admin.site.register(Work, WorkAdmin)
