from django.contrib import admin
from .models import Profile,Social_Network_Service,Icon_Mater,Acknowledgment,Language_Skill, Library_Skill, DevOps_Skill, Work, Work_Detail, Work_Language_Skill_RelationShip, Work_Library_Skill_Relationship, Work_DevOps_Skill_Relationship

class SNSInline(admin.TabularInline):
    model = Social_Network_Service
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'subtitle']}),
        ('Your information', {'fields': ['last_name', 'first_name', 'job', 'introduction']}),
        ('Photos', {'fields': ['face_photo', 'sub_photo'], 'classes': ['collapse']}),
    ]
    inlines = [SNSInline]
    list_display = ('title', 'last_name', 'first_name')

class Work_DetailInline(admin.TabularInline):
    model = Work_Detail
    extra = 1

class Work_Language_Skill_RelationShipInline(admin.TabularInline):
    model = Work_Language_Skill_RelationShip
    extra = 3
    ordering = ("sort",)

class Work_Library_Skill_RelationshipInline(admin.TabularInline):
    model = Work_Library_Skill_Relationship
    extra = 3
    ordering = ("sort",)

class Work_DevOps_Skill_RelationshipInline(admin.TabularInline):
    model = Work_DevOps_Skill_Relationship
    extra = 3
    ordering = ("sort",)

class WorkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'description']}),
        ('URL information', {'fields': ['url' ,'repository_url']}),
        ('Image', {'fields': ['image']}),
        ('private', {'fields': ['private']}),
    ]
    inlines = [Work_DetailInline, Work_Language_Skill_RelationShipInline, Work_Library_Skill_RelationshipInline, Work_DevOps_Skill_RelationshipInline]
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
