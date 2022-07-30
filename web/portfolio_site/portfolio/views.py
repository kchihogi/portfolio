"""Portfolio views.
"""
import math
from smtplib import SMTPException

from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Prefetch
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404,render
from django.views import View

from .exceptions import NeedDBMasterException
from .forms import ContactForm
from .models import Acknowledgment, Profile, Work, WorkDetail
from .models import DevOpsSkill, LanguageSkill, LibrarySkill
from .models import WorkLanguageSkillRelationShip
from .models import WorkLibrarySkillRelationship
from .models import WorkDevOpsSkillRelationship
from .models import SocialNetworkService
from .models import Bcc, Customer, MailSetting

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
        lang=LanguageSkill.objects.order_by(F('maturity').desc(nulls_last=True), 'name')
        lib=LibrarySkill.objects.order_by(F('maturity').desc(nulls_last=True), 'name')
        dev=DevOpsSkill.objects.order_by(F('maturity').desc(nulls_last=True), 'name')

        context = {'profile': prof,'acknowledgment': ack, 'lang':lang, 'lib':lib, 'dev':dev}
        return render(request, 'portfolio/about.html', context)

def success(request:HttpRequest):
    """The success page to send e-mail.

    Args:
        request (HttpRequest): Request.

    Returns:
        HttpResponse: response.
    """
    return render(request, 'portfolio/success.html')

class ContactView(View):
    """The view of contact page.
    """
    def get(self, request:HttpRequest):
        """GET.

        Returns:
            HttpResponse: response.
        """
        prof = get_list_or_404(Profile)[-1]
        try:
            self._get_settings()
        except NeedDBMasterException:
            return render(request, 'portfolio/maintenance.html')
        form = ContactForm()
        context = {'profile': prof, 'form': form}
        return render(request, 'portfolio/contact.html', context)

    def post(self, request:HttpRequest):
        """POST.

        Returns:
            HttpResponse: response.
        """
        prof = get_list_or_404(Profile)[-1]
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                self._send_mail(form)
            except NeedDBMasterException:
                return render(request, 'portfolio/maintenance.html')
            except SMTPException:
                msg = 'Failed to send mail.'
                context = {'profile': prof, 'form': form, 'error_message': msg}
                return render(request, 'portfolio/contact.html', context)
            form.save()
            self._save_customer_info(form)
            return HttpResponseRedirect(reverse('portfolio:success'))
        msg = 'Invalid inquiry.'
        context = {'profile': prof, 'form': form, 'error_message': msg}
        return render(request, 'portfolio/contact.html', context)

    def _get_settings(self):
        """Get Bcc list and the last e-mail setting.

        Raises:
            NeedDBMasterException: Bcc list is zero or email-setting is not found.

        Returns:
            QuerySet: The QuerySet of bcc list.
            MailSetting: The last e-mail setting.
        """
        bcc = Bcc.objects.all()
        setting = MailSetting.objects.filter(enable=True).last()

        if setting is None:
            raise NeedDBMasterException("MailSetting is needed.")
        if len(bcc) == 0:
            raise NeedDBMasterException("Bcc is needed.")

        return bcc, setting

    def _send_mail(self, form:ContactForm):
        """Send e-mail of the contact form.

        Raises:
            NeedDBMasterException: Bcc list is zero or email-setting is not found.
            SMTPException: An error to send e-mail.

        Args:
            form (ContactForm): The model form of the contact table.
        """
        # prep
        bcc, setting = self._get_settings()

        # make
        subject = render_to_string('mail/contact_reply_subject.txt')
        parm = {'name': form.cleaned_data["name"]
        , 'subject' : form.cleaned_data["subject"]
        , 'message' : form.cleaned_data['message']
        }
        body = render_to_string('mail/contact_reply_body.txt', parm)

        # send
        connection = get_connection()
        mail = EmailMultiAlternatives(
            subject=subject
            , body=body
            , from_email=setting.sender
            , to={form.cleaned_data["email"]}
            , connection=connection
            , bcc=bcc
        )
        mail.send()

    def _save_customer_info(self, form:ContactForm):
        """save the customer info with grouping by e-mail.

        Args:
            form (ContactForm): The model form of the contact table.
        """
        customer_name = form.cleaned_data["name"]
        customer_email = form.cleaned_data["email"]
        try:
            customer = Customer.objects.get(email=customer_email)
        except Customer.DoesNotExist:
            customer = Customer(name=customer_name, email=customer_email)
        customer.name = customer_name
        customer.count =customer.count + 1
        customer.save()
