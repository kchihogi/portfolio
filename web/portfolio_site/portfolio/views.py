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

        queryset = Work_Language_Skill_RelationShip.objects.select_related('Language_Skill')
        queryset = queryset.order_by('sort', 'Language_Skill__name')
        prefetch = Prefetch('Lang_Works', queryset=queryset, to_attr='details')
        non_p_queryset = Work.objects.filter(private=0).order_by('sort', 'title').prefetch_related(prefetch)
        p_queryset = Work.objects.exclude(private=0).order_by('sort', 'title').prefetch_related(prefetch)
        non_p_exist_cnt=non_p_queryset.count()
        p_exist_cnt = p_queryset.count()

        non_p_ref_cnt, p_ref_cnt = self._determine_work_counts(non_p_exist_cnt, p_exist_cnt)

        works = []
        if non_p_ref_cnt > 0:
            works += non_p_queryset[:non_p_ref_cnt]

        if p_ref_cnt > 0:
            works += p_queryset[:p_ref_cnt]

        context = {'profile': prof,'works': works, 'MAX_WORK' : self.MAX_WORK}
        return render(request, 'portfolio/index.html', context)

    def _determine_work_counts(self, non_private:int, private:int):
        """This calculates counts of non-private works and private works.

        If works are more than MAX(default=6) counts, it returns only MAX.
        If less, it returns counts of works.
        It balances non-private and private works.
        For example, it returns 2 for non-private and 4 for private
        when there are 2 non-private works and 6 private works in the DB, vice versa.
        For another example, it returns 3 for non-private and 3 for private
        when there are 6 non-private works and 6 private works in the DB.

        Args:
            non_private (int): non private works counts existed
            private (int): private works counts existed

        Returns:
            int: non private works counts to display
            int: private works counts to display
        """
        half_work = math.ceil(self.MAX_WORK/2)
        non_p_ref_cnt = 0
        p_ref_cnt = 0
        if non_private >= half_work and private >= half_work:
            non_p_ref_cnt = half_work
            p_ref_cnt = half_work
        elif non_private < half_work <= private:
            non_p_ref_cnt = non_private
            p_ref_cnt = self.MAX_WORK - non_private
        elif private < half_work <= non_private:
            non_p_ref_cnt = self.MAX_WORK - private
            p_ref_cnt = private
        elif non_private < half_work and private < half_work:
            non_p_ref_cnt = non_private
            p_ref_cnt = private
        else:
            non_p_ref_cnt = non_private
            p_ref_cnt = private

        return non_p_ref_cnt, p_ref_cnt

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
        lang_queryset = lang_queryset.order_by('sort', 'Language_Skill__name')
        lib_queryset = Work_Library_Skill_Relationship.objects.select_related('Library_Skill')
        lib_queryset = lib_queryset.order_by('sort', 'Library_Skill__name')
        dev_queryset = Work_DevOps_Skill_Relationship.objects.select_related('DevOps_Skill')
        dev_queryset = dev_queryset.order_by('sort', 'DevOps_Skill__name')
        lang_prefetch = Prefetch('Lang_Works', queryset=lang_queryset, to_attr='lang_details')
        lib_prefetch = Prefetch('Lib_Works', queryset=lib_queryset, to_attr='lib_details')
        dev_prefetch = Prefetch('Dev_Works', queryset=dev_queryset, to_attr='dev_details')
        works = Work.objects.order_by('sort', 'title')
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
        lang_queryset = lang_queryset.order_by('sort', 'Language_Skill__name')
        lib_queryset = Work_Library_Skill_Relationship.objects.select_related('Library_Skill')
        lib_queryset = lib_queryset.order_by('sort', 'Library_Skill__name')
        dev_queryset = Work_DevOps_Skill_Relationship.objects.select_related('DevOps_Skill')
        dev_queryset = dev_queryset.order_by('sort', 'DevOps_Skill__name')
        lang_pref = Prefetch('Lang_Works', queryset=lang_queryset, to_attr='lang_details')
        lib_pref = Prefetch('Lib_Works', queryset=lib_queryset, to_attr='lib_details')
        dev_pref = Prefetch('Dev_Works', queryset=dev_queryset, to_attr='dev_details')
        work_queryset = Work.objects.order_by('sort', 'title')
        work_queryset = work_queryset.prefetch_related(work_d_pref, lang_pref, lib_pref, dev_pref)
        work = get_object_or_404(work_queryset, pk=primary_key)
        context = {'profile': prof,'work': work}
        return render(request, 'portfolio/work.html', context)
