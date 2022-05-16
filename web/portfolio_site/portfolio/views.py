from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, get_list_or_404,render
from django.views import View
import math

from .models import Profile, Work, Work_Language_Skill_RelationShip, Work_Library_Skill_Relationship, Work_DevOps_Skill_Relationship, Work_Detail

from utils.logger import Logger
log = Logger("mylog")

class IndexView(View):
    def get(self, request):
        prof = get_list_or_404(Profile)[-1]

        MAX_WORK = 6
        HALF_WORK = math.ceil(MAX_WORK/2)
        works = []

        prefetch = Prefetch('Lang_Works', queryset=Work_Language_Skill_RelationShip.objects.select_related('Language_Skill').order_by('sort'), to_attr='details')
        tmpworks=Work.objects.filter(private=0).order_by('sort').prefetch_related(prefetch)

        if tmpworks.count() >= HALF_WORK:
            tmpworks = tmpworks[:HALF_WORK]

        works += tmpworks
        works += Work.objects.exclude(private=0).order_by('sort').prefetch_related(prefetch)[:MAX_WORK - tmpworks.count()]

        context = {'profile': prof,'works': works, 'MAX_WORK' : MAX_WORK}
        return render(request, 'portfolio/index.html', context)

class WorksView(View):
    def get(self, request):
        prof = get_list_or_404(Profile)[-1]

        works = []

        lang_prefetch = Prefetch('Lang_Works', queryset=Work_Language_Skill_RelationShip.objects.select_related('Language_Skill').order_by('sort'), to_attr='lang_details')
        lib_prefetch = Prefetch('Lib_Works', queryset=Work_Library_Skill_Relationship.objects.select_related('Library_Skill').order_by('sort'), to_attr='lib_details')
        dev_prefetch = Prefetch('Dev_Works', queryset=Work_DevOps_Skill_Relationship.objects.select_related('DevOps_Skill').order_by('sort'), to_attr='dev_details')
        works = Work.objects.order_by('sort').prefetch_related(lang_prefetch, lib_prefetch, dev_prefetch)

        context = {'profile': prof,'works': works}
        return render(request, 'portfolio/works.html', context)

class WorkView(View):
    def get(self, request, pk):
        prof = get_list_or_404(Profile)[-1]
        work_detail_prefetch = Prefetch('Work_Details', queryset=Work_Detail.objects.all(), to_attr='work_details')
        lang_prefetch = Prefetch('Lang_Works', queryset=Work_Language_Skill_RelationShip.objects.select_related('Language_Skill').order_by('sort'), to_attr='lang_details')
        lib_prefetch = Prefetch('Lib_Works', queryset=Work_Library_Skill_Relationship.objects.select_related('Library_Skill').order_by('sort'), to_attr='lib_details')
        dev_prefetch = Prefetch('Dev_Works', queryset=Work_DevOps_Skill_Relationship.objects.select_related('DevOps_Skill').order_by('sort'), to_attr='dev_details')
        work = get_object_or_404(Work.objects.order_by('sort').prefetch_related(work_detail_prefetch, lang_prefetch, lib_prefetch, dev_prefetch), pk=pk)
        context = {'profile': prof,'work': work}
        return render(request, 'portfolio/work.html', context)
