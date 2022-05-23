"""Portfolio views.
"""
import math

from django.db.models import Prefetch
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, get_list_or_404,render
from django.views import View

from utils.logger import Logger

from .models import Profile, Work, Work_Detail
from .models import Work_Language_Skill_RelationShip
from .models import Work_Library_Skill_Relationship
from .models import Work_DevOps_Skill_Relationship

log = Logger("mylog")

class IndexView(View):
    """The view of the index page.
    """

    MAX_WORK = 6
    def get(self, request:HttpRequest):
        """GET.

        Args:
            request (HttpRequest): request.

        Returns:
            HttpResponse: response.
        """
        prof = get_list_or_404(Profile)[-1]

        half_work = math.ceil(self.MAX_WORK/2)
        works = []

        queryset = Work_Language_Skill_RelationShip.objects.select_related('Language_Skill')
        queryset = queryset.order_by('sort')
        prefetch = Prefetch('Lang_Works', queryset=queryset, to_attr='details')
        tmpworks=Work.objects.filter(private=0).order_by('sort').prefetch_related(prefetch)

        if tmpworks.count() >= half_work:
            tmpworks = tmpworks[:half_work]

        works += tmpworks
        tmpworks = Work.objects.exclude(private=0).order_by('sort').prefetch_related(prefetch)
        works += tmpworks[:self.MAX_WORK - tmpworks.count()]

        context = {'profile': prof,'works': works, 'MAX_WORK' : self.MAX_WORK}
        return render(request, 'portfolio/index.html', context)

class WorksView(View):
    """The view of works page.
    """
    def get(self, request:HttpRequest):
        """GET.

        Args:
            request (HttpRequest): request.

        Returns:
            HttpRespose: response.
        """
        prof = get_list_or_404(Profile)[-1]

        works = []

        lang_queryset = Work_Language_Skill_RelationShip.objects.select_related('Language_Skill')
        lang_queryset = lang_queryset.order_by('sort')
        lib_queryset = Work_Library_Skill_Relationship.objects.select_related('Library_Skill')
        lib_queryset = lib_queryset.order_by('sort')
        dev_queryset = Work_DevOps_Skill_Relationship.objects.select_related('DevOps_Skill')
        dev_queryset = dev_queryset.order_by('sort')
        lang_prefetch = Prefetch('Lang_Works', queryset=lang_queryset, to_attr='lang_details')
        lib_prefetch = Prefetch('Lib_Works', queryset=lib_queryset, to_attr='lib_details')
        dev_prefetch = Prefetch('Dev_Works', queryset=dev_queryset, to_attr='dev_details')
        works = Work.objects.order_by('sort')
        works = works.prefetch_related(lang_prefetch, lib_prefetch, dev_prefetch)

        context = {'profile': prof,'works': works}
        return render(request, 'portfolio/works.html', context)

class WorkView(View):
    """The view of work page.
    """
    def get(self, request:HttpRequest, primary_key:int):
        """GET.

        Args:
            request (HttpRequest): request.
            primary_key (int): primary key of the Work.

        Returns:
            HttpResponse: response.
        """
        prof = get_list_or_404(Profile)[-1]
        work_d_queryset = Work_Detail.objects.all()
        work_d_pref = Prefetch('Work_Details', queryset=work_d_queryset, to_attr='work_details')
        lang_queryset = Work_Language_Skill_RelationShip.objects.select_related('Language_Skill')
        lang_queryset = lang_queryset.order_by('sort')
        lib_queryset = Work_Library_Skill_Relationship.objects.select_related('Library_Skill')
        lib_queryset = lib_queryset.order_by('sort')
        dev_queryset = Work_DevOps_Skill_Relationship.objects.select_related('DevOps_Skill')
        dev_queryset = dev_queryset.order_by('sort')
        lang_pref = Prefetch('Lang_Works', queryset=lang_queryset, to_attr='lang_details')
        lib_pref = Prefetch('Lib_Works', queryset=lib_queryset, to_attr='lib_details')
        dev_pref = Prefetch('Dev_Works', queryset=dev_queryset, to_attr='dev_details')
        work_queryset = Work.objects.order_by('sort')
        work_queryset = work_queryset.prefetch_related(work_d_pref, lang_pref, lib_pref, dev_pref)
        work = get_object_or_404(work_queryset, pk=primary_key)
        context = {'profile': prof,'work': work}
        return render(request, 'portfolio/work.html', context)
