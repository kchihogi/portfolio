"""This module set up the admin page of django site.
"""
from django.contrib import admin

from .models import Profile,SocialNetworkService,IconMater,Acknowledgment
from .models import LanguageSkill, LibrarySkill, DevOpsSkill
from .models import Work, WorkDetail
from .models import WorkLanguageSkillRelationShip
from .models import WorkLibrarySkillRelationship
from .models import WorkDevOpsSkillRelationship

class SNSInline(admin.TabularInline):
    """An inline input form for SNS.
    """
    model = SocialNetworkService
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    """The setting of Profile.
    """
    fieldsets = [
        (None,               {'fields': ['title', 'subtitle']}),
        ('Your information', {'fields': [
            'last_name', 'first_name', 'job'
            , 'introduction', 'gender', 'birthday'
            , 'email', 'phone', 'address'
            ]}),
        ('Photos', {'fields': ['face_photo', 'sub_photo'], 'classes': ['collapse']}),
    ]
    inlines = [SNSInline]
    list_display = ('title', 'last_name', 'first_name')

class WorkDetailInline(admin.TabularInline):
    """An inline input form for work details.
    """
    model = WorkDetail
    extra = 1

class WorkLanguageSkillRelationShipInline(admin.TabularInline):
    """An inline input form for language skills.
    """
    model = WorkLanguageSkillRelationShip
    extra = 3
    ordering = ("sort",)

class WorkLibrarySkillRelationshipInline(admin.TabularInline):
    """An inline input form fofr library skills.
    """
    model = WorkLibrarySkillRelationship
    extra = 3
    ordering = ("sort",)

class WorkDevOpsSkillRelationshipInline(admin.TabularInline):
    """An inline input form for DevOps skills.
    """
    model = WorkDevOpsSkillRelationship
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
admin.site.register(IconMater)
admin.site.register(Acknowledgment)
admin.site.register(LanguageSkill)
admin.site.register(LibrarySkill)
admin.site.register(DevOpsSkill)
admin.site.register(Work, WorkAdmin)
