"""Portfolio views.
"""
import math

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, get_list_or_404,render
from django.views import View

from .models import Acknowledgment, Profile, Work, WorkDetail
from .models import WorkLanguageSkillRelationShip
from .models import WorkLibrarySkillRelationship
from .models import WorkDevOpsSkillRelationship
from .models import SocialNetworkService

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

        queryset = WorkLanguageSkillRelationShip.objects.select_related('language_skill')
        queryset = queryset.order_by('sort', 'language_skill__name')
        prefetch = Prefetch('lang_works', queryset=queryset, to_attr='details')
        n_p_qs = Work.objects.filter(private=0).order_by('sort', 'title').prefetch_related(prefetch)
        p_qs = Work.objects.exclude(private=0).order_by('sort', 'title').prefetch_related(prefetch)
        non_p_exist_cnt=n_p_qs.count()
        p_exist_cnt = p_qs.count()

        non_p_ref_cnt, p_ref_cnt = self._determine_work_counts(non_p_exist_cnt, p_exist_cnt)

        works = []
        if non_p_ref_cnt > 0:
            works += n_p_qs[:non_p_ref_cnt]

        if p_ref_cnt > 0:
            works += p_qs[:p_ref_cnt]

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

    PAGENATION_COUNT=12
    def get(self, request:HttpRequest):
        """GET.

        Args:
            request (HttpRequest): request.

        Returns:
            HttpRespose: response.
        """
        prof = get_list_or_404(Profile)[-1]

        works = []

        lang_queryset = WorkLanguageSkillRelationShip.objects.select_related('language_skill')
        lang_queryset = lang_queryset.order_by('sort', 'language_skill__name')
        lib_queryset = WorkLibrarySkillRelationship.objects.select_related('library_skill')
        lib_queryset = lib_queryset.order_by('sort', 'library_skill__name')
        dev_queryset = WorkDevOpsSkillRelationship.objects.select_related('dev_ops_skill')
        dev_queryset = dev_queryset.order_by('sort', 'dev_ops_skill__name')
        lang_prefetch = Prefetch('lang_works', queryset=lang_queryset, to_attr='lang_details')
        lib_prefetch = Prefetch('lib_works', queryset=lib_queryset, to_attr='lib_details')
        dev_prefetch = Prefetch('dev_works', queryset=dev_queryset, to_attr='dev_details')
        works = Work.objects.order_by('sort', 'title')
        works = works.prefetch_related(lang_prefetch, lib_prefetch, dev_prefetch)

        # pagenateの実行
        paginator = Paginator(works, self.PAGENATION_COUNT)
        page = request.GET.get('page')

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context = {'profile': prof,'works': page_obj.object_list, 'page_obj': page_obj}
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
        work_d_queryset = WorkDetail.objects.all()
        work_d_pref = Prefetch('work_details', queryset=work_d_queryset, to_attr='details')
        lang_queryset = WorkLanguageSkillRelationShip.objects.select_related('language_skill')
        lang_queryset = lang_queryset.order_by('sort', 'language_skill__name')
        lib_queryset = WorkLibrarySkillRelationship.objects.select_related('library_skill')
        lib_queryset = lib_queryset.order_by('sort', 'library_skill__name')
        dev_queryset = WorkDevOpsSkillRelationship.objects.select_related('dev_ops_skill')
        dev_queryset = dev_queryset.order_by('sort', 'dev_ops_skill__name')
        lang_pref = Prefetch('lang_works', queryset=lang_queryset, to_attr='lang_details')
        lib_pref = Prefetch('lib_works', queryset=lib_queryset, to_attr='lib_details')
        dev_pref = Prefetch('dev_works', queryset=dev_queryset, to_attr='dev_details')
        work_queryset = Work.objects.order_by('sort', 'title')
        work_queryset = work_queryset.prefetch_related(work_d_pref, lang_pref, lib_pref, dev_pref)
        work = get_object_or_404(work_queryset, pk=primary_key)
        context = {'profile': prof,'work': work}
        return render(request, 'portfolio/work.html', context)

class AboutView(View):
    """The view of the about page.
    """

    def get(self, request:HttpRequest):
        """GET.

        Args:
            request (HttpRequest): request.

        Returns:
            HttpResponse: response.
        """
        qs = SocialNetworkService.objects.select_related('icon_master')
        qs = qs.order_by('name')
        pref = Prefetch('profiles', queryset=qs, to_attr='sns')
        p_qs = Profile.objects.prefetch_related(pref)
        prof = get_list_or_404(p_qs)[-1]
        ack = Acknowledgment.objects.filter(enable=1)[0:]

        context = {'profile': prof,'acknowledgment': ack}
        return render(request, 'portfolio/about.html', context)
