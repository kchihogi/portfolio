"""UT Test module for the Works View."""
from urllib import parse

from django.test import TestCase
from django.urls import reverse

from . import utils

# Views Tests

class WorksViewTest(TestCase):
    """This class is an object to test the WorksView."""

    def test_no_profile(self):
        """If no profile resistered, the works page returns 404.
        """
        response = self.client.get(reverse('portfolio:works'))
        self.assertEqual(response.status_code, 404)

    def test_no_work(self):
        """If no works, the works page contains "No works are available.
        """
        profile = utils.create_profile()
        response = self.client.get(reverse('portfolio:works'))
        self.assertContains(response=response, text=profile.title)
        self.assertContains(response=response, text='No works are available.')
        self.assertQuerysetEqual(
            response.context['works'],
            [],
        )

    def test_no_skills_works(self):
        """If no skills related to works, works are listed without skills.
        """
        utils.create_profile()
        private_work = 0
        lang=[]
        work_a = utils.create_work('WorkA', private_work,sort=0)
        utils.relate_language_skills(work=work_a, languages=lang)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        utils.relate_language_skills(work=work_b, languages=lang)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        utils.relate_language_skills(work=work_c, languages=lang)
        work_d = utils.create_work('WorkD', private_work,sort=0)
        utils.relate_language_skills(work=work_d, languages=lang)
        work_e = utils.create_work('WorkE', private_work,sort=0)
        utils.relate_language_skills(work=work_e, languages=lang)
        work_f = utils.create_work('WorkF', private_work,sort=0)
        utils.relate_language_skills(work=work_f, languages=lang)
        response = self.client.get(reverse('portfolio:works'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_lang_sorted(self):
        """This tests that language skills are sorted by its sort column in a work.

        The value of the sort can be duplicated.
        """
        utils.create_profile()
        utils.add_language_skills()
        private_work = 0
        langs = []
        lang = [('C#', 2),('Powershell', 1),('Java', 3)]
        work_a = utils.create_work('WorkA', private_work,sort=0)
        utils.relate_language_skills(work=work_a, languages=lang)
        langs.append(lang)
        response = self.client.get(reverse('portfolio:works'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a],
        )

        utils.assert_skills(
            response.context['works'],
            "lang_details",
            "language_skill.name",
            "sort",
            langs,
        )


    def test_lib_sorted(self):
        """This tests that library skills are sorted by its sort column in a work.

        The value of the sort can be duplicated.
        """
        utils.create_profile()
        utils.add_library_skills()
        private_work = 0
        libs = []
        lib = [('Django', 2),('.Net Framework', 1),('F社標準ライブラリ', 3)]
        work_a = utils.create_work('WorkA', private_work,sort=0)
        utils.relate_lib_skills(work=work_a, libs=lib)
        libs.append(lib)
        response = self.client.get(reverse('portfolio:works'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a],
        )

        utils.assert_skills(
            response.context['works'],
            "lib_details",
            "library_skill.name",
            "sort",
            libs,
        )

    def test_dev_ops_sorted(self):
        """This tests that DevOps skills are sorted by its sort column in a work.

        The value of the sort can be duplicated.
        """
        utils.create_profile()
        utils.add_dev_ops_skills()
        private_work = 0
        devs = []
        dev = [('Visual Studio', 2),('VS Code', 1),('SQL Server Management Studio', 3)]
        work_a = utils.create_work('WorkA', private_work,sort=0)
        utils.relate_dev_ops_skills(work=work_a, dev_ops=dev)
        devs.append(dev)
        response = self.client.get(reverse('portfolio:works'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a],
        )

        utils.assert_skills(
            response.context['works'],
            "dev_details",
            "dev_ops_skill.name",
            "sort",
            devs,
        )

    def test_all_skills_mixed_works(self):
        """Language, library, and DevOps skills are all listed in a work.
        """
        utils.create_personal_base()

        private_work = 0
        langs = []
        libs = []
        devs = []
        work_a = utils.create_work('WorkA', private_work,sort=3)
        work_b = utils.create_work('WorkB', private_work,sort=2)
        work_c = utils.create_work('WorkC', private_work,sort=1)

        lang = [('C#', 2),('Powershell', 1),('Java', 3)]
        lib = [('Django', 2),('.Net Framework', 1),('F社標準ライブラリ', 3)]
        dev = [('SQL Server Management Studio', 0),('VS Code', 0), ('Visual Studio', 0)]
        utils.relate_dev_ops_skills(work=work_c, dev_ops=dev)
        utils.relate_lib_skills(work=work_c, libs=lib)
        utils.relate_language_skills(work=work_c, languages=lang)
        langs.append(lang)
        libs.append(lib)
        devs.append(dev)

        lang = [('C#', 3),('Powershell', 99),('Java', 1)]
        lib = [('Django', 3),('.Net Framework', 2),('F社標準ライブラリ', 1)]
        dev = [('Visual Studio', 2),('VS Code', 70),('SQL Server Management Studio', 3)]
        utils.relate_dev_ops_skills(work=work_b, dev_ops=dev)
        utils.relate_lib_skills(work=work_b, libs=lib)
        utils.relate_language_skills(work=work_b, languages=lang)
        langs.append(lang)
        libs.append(lib)
        devs.append(dev)

        lang = [('C#', 1),('Powershell', 2),('Java', 3)]
        lib = [('.Net Framework', 2), ('Django', 2), ('F社標準ライブラリ', 2)]
        dev = [('Visual Studio', 3),('VS Code', 2),('SQL Server Management Studio', 1)]
        utils.relate_dev_ops_skills(work=work_a, dev_ops=dev)
        utils.relate_lib_skills(work=work_a, libs=lib)
        utils.relate_language_skills(work=work_a, languages=lang)
        langs.append(lang)
        libs.append(lib)
        devs.append(dev)

        response = self.client.get(reverse('portfolio:works'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_c, work_b, work_a],
        )

        utils.assert_skills_set(
            response.context['works'],
            langs,
            libs,
            devs,
        )

    def test_pagination_zero_work(self):
        """This tests that pagination returns 1 when there are no works.
        """
        utils.create_profile()
        response = self.client.get(reverse('portfolio:works'))
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 0)
        self.assertEqual(page_obj.paginator.num_pages, 1)
        self.assertEqual(page_obj.number, 1)

    def test_pagination_one_work(self):
        """This tests that pagination returns 1 when there is a work.
        """
        utils.create_profile()
        private_work = 0
        utils.create_work('WorkA', private_work,sort=0)
        response = self.client.get(reverse('portfolio:works'))
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 1)
        self.assertEqual(page_obj.paginator.num_pages, 1)
        self.assertEqual(page_obj.number, 1)

    def test_pagination_eleven_works(self):
        """This tests that pagination returns 1 when there are 11 works.
        """
        utils.create_profile()
        private_work = 0
        for i in range(11):
            utils.create_work(f'Work{str(i)}', private_work,sort=0)
        response = self.client.get(reverse('portfolio:works'))
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 11)
        self.assertEqual(page_obj.paginator.num_pages, 1)
        self.assertEqual(page_obj.number, 1)

    def test_pagination_twelve_works(self):
        """This tests that pagination returns 1 when there are 12 works.
        """
        utils.create_profile()
        private_work = 0
        for i in range(12):
            utils.create_work(f'Work{str(i)}', private_work,sort=0)
        response = self.client.get(reverse('portfolio:works'))
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 12)
        self.assertEqual(page_obj.paginator.num_pages, 1)
        self.assertEqual(page_obj.number, 1)

    def test_pagination_thirteen_works(self):
        """This tests that pagination returns 2 when there are 13 works.
        """
        utils.create_profile()
        private_work = 0
        for i in range(13):
            utils.create_work(f'Work{str(i)}', private_work,sort=0)
        response = self.client.get(reverse('portfolio:works'))
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 13)
        self.assertEqual(page_obj.paginator.num_pages, 2)
        self.assertEqual(page_obj.number, 1)
        url = reverse('portfolio:works')
        url = '?'.join([url,parse.urlencode(dict(page='2'))])
        response = self.client.get(url)
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.number, 2)

    def test_pagination_three_hundreds_works(self):
        """This tests that pagination returns 25 when there are 300 works.
        """
        utils.create_profile()
        private_work = 0
        for i in range(300):
            utils.create_work(f'Work{str(i)}', private_work,sort=0)
        response = self.client.get(reverse('portfolio:works'))
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 300)
        self.assertEqual(page_obj.paginator.num_pages, 25)
        self.assertEqual(page_obj.number, 1)

    def test_pagination_no_int_request(self):
        """Pagination returns the first page with a request having a not int parameter.
        """
        utils.create_profile()
        private_work = 0
        for i in range(20):
            utils.create_work(f'Work{str(i)}', private_work,sort=0)
        url = reverse('portfolio:works')
        url = '?'.join([url, parse.urlencode(dict(page='hogehoge'))])
        response = self.client.get(url)
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 20)
        self.assertEqual(page_obj.paginator.num_pages, 2)
        self.assertEqual(page_obj.number, 1)

    def test_pagination_unknown_page_request(self):
        """Pagination returns the last page with a request having an unknown page number.
        """
        utils.create_profile()
        private_work = 0
        for i in range(20):
            utils.create_work(f'Work{str(i)}', private_work,sort=0)
        url = reverse('portfolio:works')
        url = '?'.join([url,parse.urlencode(dict(page='999'))])
        response = self.client.get(url)
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 20)
        self.assertEqual(page_obj.paginator.num_pages, 2)
        self.assertEqual(page_obj.number, 2)
        url = reverse('portfolio:works')
        url = '?'.join([url,parse.urlencode(dict(page='-999'))])
        response = self.client.get(url)
        page_obj = response.context['page_obj']
        self.assertEqual(page_obj.paginator.count, 20)
        self.assertEqual(page_obj.paginator.num_pages, 2)
        self.assertEqual(page_obj.number, 2)
