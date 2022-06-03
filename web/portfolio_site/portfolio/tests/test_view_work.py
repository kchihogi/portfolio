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
        utils.cretet_profile()
        response = self.client.get(reverse('portfolio:work', kwargs=dict(primary_key='1')))
        self.assertEqual(response.status_code, 404)

    def test_str_primary_key_request(self):
        """If no works, the work page returns 404.
        """
        utils.cretet_profile()
        url = reverse('portfolio:work', kwargs=dict(primary_key='1'))
        url = url.replace('1', 'hogehoge')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_work_with_no_details(self):
        """This tests to get a work without details.
        """
        profile = utils.cretet_profile()
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

        utils.assert_skills(
            [response.context['work']],
            "lang_details",
            "language_skill.name",
            "sort",
            langs,
        )

        utils.assert_skills(
            [response.context['work']],
            "lib_details",
            "library_skill.name",
            "sort",
            libs,
        )

        utils.assert_skills(
            [response.context['work']],
            "dev_details",
            "dev_ops_skill.name",
            "sort",
            devs,
        )

    def test_get_work_with_songle_detail(self):
        """This tests to get a work with a detail.
        """
        utils.cretet_profile()
        utils.add_language_skills()
        utils.add_library_skills()
        utils.add_dev_ops_skills()

        private_work = 0
        work_a = utils.create_work('WorkA', private_work,sort=0)
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
        sub='サブタイトル'
        detail = utils.relate_work_detail(work_a,sub,proc,start,end,desc)
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

        utils.assert_skills(
            [response.context['work']],
            "lang_details",
            "language_skill.name",
            "sort",
            langs,
        )

        utils.assert_skills(
            [response.context['work']],
            "lib_details",
            "library_skill.name",
            "sort",
            libs,
        )

        utils.assert_skills(
            [response.context['work']],
            "dev_details",
            "dev_ops_skill.name",
            "sort",
            devs,
        )

    def test_get_work_with_multi_details(self):
        """This tests to get a work with some details.
        """
        utils.cretet_profile()
        utils.add_language_skills()
        utils.add_library_skills()
        utils.add_dev_ops_skills()

        private_work = 0
        work_a = utils.create_work('WorkA', private_work,sort=0)
        details = []
        desc=""
        for i in range(300):
            start = timezone.now() + datetime.timedelta(days=-365)
            end = timezone.now()
            proc='工程A,工程B,工程C'
            desc+='詳細情報'
            sub=f'サブタイトル{str(i)}'
            detail = utils.relate_work_detail(work_a,sub,proc,start,end,desc)
            details.append(detail)

        response = self.client.get(reverse('portfolio:work', kwargs=dict(primary_key=work_a.pk)))

        self.assertEqual(
            response.context['work'],
            work_a,
        )

        self.assertEqual(response.context['work'].details, details)
