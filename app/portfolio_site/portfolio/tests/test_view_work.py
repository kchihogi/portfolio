"""UT Test module for the Work View."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from . import utils

# Views Tests

class WorkViewTest(TestCase):
    """This class is an object to test the WorkView."""

    def test_no_profile(self):
        """If no profile resistered, the works page returns 404.
        """
        response = self.client.get(reverse('portfolio:work', kwargs=dict(primary_key='1')))
        self.assertEqual(response.status_code, 404)

    def test_no_work(self):
        """If no works, the work page returns 404.
        """
        utils.create_profile()
        response = self.client.get(reverse('portfolio:work', kwargs=dict(primary_key='1')))
        self.assertEqual(response.status_code, 404)

    def test_str_primary_key_request(self):
        """If no works, the work page returns 404.
        """
        utils.create_profile()
        url = reverse('portfolio:work', kwargs=dict(primary_key='1'))
        url = url.replace('1', 'hogehoge')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_work_with_no_details(self):
        """This tests to get a work without details.
        """
        profile = utils.create_profile()
        private_work = 0
        work_a = utils.create_work('WorkA', private_work,sort=0)
        response = self.client.get(reverse('portfolio:work', kwargs=dict(primary_key=work_a.pk)))
        self.assertContains(response=response, text=profile.title)
        self.assertEqual(
            response.context['work'],
            work_a,
        )

        self.assertEqual(response.context['work'].details, [])

        langs = []
        libs = []
        devs = []
        langs.append([])
        libs.append([])
        devs.append([])

        utils.assert_skills_set(
            [response.context['work']],
            langs,
            libs,
            devs,
        )

    def test_get_work_with_songle_detail(self):
        """This tests to get a work with a detail.
        """
        utils.create_profile()
        utils.add_language_skills()
        utils.add_library_skills()
        utils.add_dev_ops_skills()

        work_a = utils.create_work('WorkA', private_work=0,sort=0)
        details = []
        langs = []
        libs = []
        devs = []
        lang = [('C#', 2),('Powershell', 1),('Java', 3)]
        lib = [('Django', 2),('.Net Framework', 1),('F社標準ライブラリ', 3)]
        dev = [('SQL Server Management Studio', 0),('VS Code', 0), ('Visual Studio', 0)]
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        proc='工程A,工程B,工程C'
        desc='詳細情報'
        detail = utils.relate_work_detail(work_a,proc,start,end,desc)
        utils.relate_dev_ops_skills(work=work_a, dev_ops=dev)
        utils.relate_lib_skills(work=work_a, libs=lib)
        utils.relate_language_skills(work=work_a, languages=lang)
        details.append(detail)
        langs.append(lang)
        libs.append(lib)
        devs.append(dev)

        response = self.client.get(reverse('portfolio:work', kwargs=dict(primary_key=work_a.pk)))

        self.assertEqual(
            response.context['work'],
            work_a,
        )

        self.assertEqual(response.context['work'].details, details)

        utils.assert_skills_set(
            [response.context['work']],
            langs,
            libs,
            devs,
        )

    def test_get_work_with_multi_details(self):
        """This tests to get a work with some details.
        """
        utils.create_personal_base()

        private_work = 0
        work_a = utils.create_work('WorkA', private_work,sort=0)
        details = []
        desc=""
        for i in range(300):
            start = timezone.now() + datetime.timedelta(days=-365)
            end = timezone.now()
            proc='工程A,工程B,工程C'
            desc+=f'詳細情報{i}'
            detail = utils.relate_work_detail(work_a,proc,start,end,desc)
            details.append(detail)

        response = self.client.get(reverse('portfolio:work', kwargs=dict(primary_key=work_a.pk)))

        self.assertEqual(
            response.context['work'],
            work_a,
        )

        self.assertEqual(response.context['work'].details, details)
