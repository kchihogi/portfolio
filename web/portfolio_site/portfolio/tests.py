"""UT Test module for portfolio application."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Profile, Work, Work_Detail
from .models import Language_Skill, Work_Language_Skill_RelationShip
from .models import Library_Skill, Work_Library_Skill_Relationship
from .models import DevOps_Skill, Work_DevOps_Skill_Relationship

# private methods
def _cretet_profile():
    """This cretes fixed profile.

    Returns:
        Profile: the model of Profile created.
    """
    prof = Profile(title = 'タイトル', subtitle = 'サブタイトル', first_name = 'ミカド', last_name = '赤城')
    prof.job = 'システムエンジニア'
    intro = ''
    for i in range(300):
        intro += str(i%10)
    prof.introduction = intro
    prof.face_photo = 'profile/face.png'
    prof.sub_photo = 'profile/sub.png'
    prof.save()
    return prof

def _create_work(work_name:str, private_work:int, start:datetime, end:datetime, sort:int=0):
    """This cretes work with foreign relations.

    Args:
        work_name (str): a name of work
        private_work (int): 0 for no private work. 1 for private work.
        start (datetime): start datetime when a project started.
        end (datetime): end datetime when a project ended.
        sort (int, optional): sort number to displaye the web page. Defaults to 0.

    Returns:
        Work: the model of Work created.
    """
    desc = ''
    for i in range(300):
        if i%10 == 0 and i !=0:
            desc += '\n'
        else:
            desc += 'Z'
    work = Work()
    work.title = work_name
    work.image='works/' + work_name + '.png'
    work.private=private_work
    work.description = desc
    work.url='https://dummy_url'
    work.repository_url='https://dummy_repourl'
    work.sort=sort
    work.save()

    work_detail = Work_Detail()
    work_detail.Work_id=work.pk
    work_detail.sub_titile='サブタイトル'
    work_detail.start_date=start
    work_detail.end_date=end
    work_detail.processes='工程A,工程B,工程C'
    work_detail.detail_description= '詳細情報'
    work_detail.save()
    return work

def _add_language_skills(work:Work, languages:list[str]):
    """This cretes relationship with work and language skills.

    Args:
        work (Work): the model of work.
        languages (list[str]): a list of language name.
    """
    if languages is not None:
        for record in Language_Skill.objects.all():
            for language in languages:
                if record.name == language:
                    relation = Work_Language_Skill_RelationShip()
                    relation.Work_id=work.pk
                    relation.Language_Skill_id=record.pk
                    relation.sort=0
                    relation.save()

def _add_lib_skills(work:Work, libs:list[str]):
    """This cretes relationship with work and libs skills.

    Args:
        work (Work): the model of work.
        libs (list[str]): a list of library name.
    """
    if libs is not None:
        for record in Library_Skill.objects.all():
            for lib in libs:
                if record.name == lib:
                    relation = Work_Library_Skill_Relationship()
                    relation.Work_id=work.pk
                    relation.Library_Skill_id=record.pk
                    relation.sort=0
                    relation.save()

def _add_dev_ops_skills(work:Work, dev_ops:list[str]):
    """This cretes relationship with work and dev_ops skills.

    Args:
        work (Work): the model of work.
        dev_ops (list[str]): a list of dev_ops skill name.
    """
    if dev_ops is not None:
        for record in DevOps_Skill.objects.all():
            for dev in dev_ops:
                if record.name == dev:
                    relation = Work_DevOps_Skill_Relationship()
                    relation.Work_id=work.pk
                    relation.DevOps_Skill_id=record.pk
                    relation.sort=0
                    relation.save()

# Views Tests

class IndexViewTest(TestCase):
    """This class is an object to test the IndexView."""

    def test_no_profile(self):
        """If no profile resistered, the index page returns 404.
        """
        response = self.client.get(reverse('portfolio:index'))
        self.assertEqual(response.status_code, 404)

    def test_no_work(self):
        """If no works, the index page contains "No works are available.
        """
        profile = _cretet_profile()
        response = self.client.get(reverse('portfolio:index'))
        self.assertContains(response=response, text=profile.title)
        self.assertContains(response=response, text='No works are available.')
        self.assertQuerysetEqual(
            response.context['works'],
            [],
        )

    def test_three_no_private_works(self):
        """The index page shows three no private works.
        """
        _cretet_profile()
        private_work = 0
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c],
        )

    def test_six_no_private_works(self):
        """The index page shows six no private works.
        """
        _cretet_profile()
        private_work = 0
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', private_work, start, end,sort=0)
        work_d = _create_work('WorkD', private_work, start, end,sort=0)
        work_e = _create_work('WorkE', private_work, start, end,sort=0)
        work_f = _create_work('WorkF', private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_seven_no_private_works(self):
        """The index page shows only six no private works, not seven works.
        """
        _cretet_profile()
        private_work = 0
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', private_work, start, end,sort=0)
        work_d = _create_work('WorkD', private_work, start, end,sort=0)
        work_e = _create_work('WorkE', private_work, start, end,sort=0)
        work_f = _create_work('WorkF', private_work, start, end,sort=0)
        _create_work('WorkG', private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_three_private_works(self):
        """The index page shows three private works.
        """
        _cretet_profile()
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c],
        )

    def test_six_private_works(self):
        """The index page shows six private works.
        """
        _cretet_profile()
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', private_work, start, end,sort=0)
        work_d = _create_work('WorkD', private_work, start, end,sort=0)
        work_e = _create_work('WorkE', private_work, start, end,sort=0)
        work_f = _create_work('WorkF', private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_seven_private_works(self):
        """The index page shows only six private works, not seven works.
        """
        _cretet_profile()
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', private_work, start, end,sort=0)
        work_d = _create_work('WorkD', private_work, start, end,sort=0)
        work_e = _create_work('WorkE', private_work, start, end,sort=0)
        work_f = _create_work('WorkF', private_work, start, end,sort=0)
        _create_work('WorkG', private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_three_private_and_three_non_works(self):
        """The index page shows three no private works and three private works.
        """
        _cretet_profile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', non_private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', non_private_work, start, end,sort=0)
        work_d = _create_work('WorkD', private_work, start, end,sort=0)
        work_e = _create_work('WorkE', non_private_work, start, end,sort=0)
        work_f = _create_work('WorkF', private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_c, work_e, work_b, work_d, work_f],
        )

    def test_two_private_and_two_non_works(self):
        """The index page shows two no private works and two private works.
        """
        _cretet_profile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', non_private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', non_private_work, start, end,sort=0)
        work_d = _create_work('WorkD', private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_c, work_b, work_d],
        )

    def test_two_private_and_five_non_works(self):
        """The index page shows four non private works and two private works.
        """
        _cretet_profile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', non_private_work, start, end,sort=0)
        work_d = _create_work('WorkD', non_private_work, start, end,sort=0)
        work_e = _create_work('WorkE', non_private_work, start, end,sort=0)
        work_f = _create_work('WorkF', non_private_work, start, end,sort=0)
        _create_work('WorkG', non_private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_c, work_d, work_e, work_f, work_a, work_b],
        )

    def test_five_private_and_two_non_works(self):
        """The index page shows two non private works and four private works.
        """
        _cretet_profile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', private_work, start, end,sort=0)
        work_d = _create_work('WorkD', private_work, start, end,sort=0)
        _create_work('WorkE', private_work, start, end,sort=0)
        work_f = _create_work('WorkF', non_private_work, start, end,sort=0)
        work_g = _create_work('WorkG', non_private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_f, work_g, work_a, work_b, work_c, work_d],
        )

    def test_four_private_and_four_non_works(self):
        """The index page shows three non private works and three private works.
        """
        _cretet_profile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=0)
        work_b = _create_work('WorkB', private_work, start, end,sort=0)
        work_c = _create_work('WorkC', private_work, start, end,sort=0)
        _create_work('WorkD', private_work, start, end,sort=0)
        work_e = _create_work('WorkE', non_private_work, start, end,sort=0)
        work_f = _create_work('WorkF', non_private_work, start, end,sort=0)
        work_g = _create_work('WorkG', non_private_work, start, end,sort=0)
        _create_work('WorkH', non_private_work, start, end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_e, work_f, work_g, work_a, work_b, work_c],
        )

    def test_works_sorted(self):
        """This tests that works are sorted by the sort column.

        The value of the sort can be duplicated.
        """
        _cretet_profile()
        private_work = 0
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _create_work('WorkA', private_work, start, end,sort=2)
        work_b = _create_work('WorkB', private_work, start, end,sort=1)
        work_c = _create_work('WorkC', private_work, start, end,sort=3)
        work_d = _create_work('WorkD', private_work, start, end,sort=2)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_b, work_a, work_d, work_c],
        )

# Models Tests

# class ProfileModelTests(TestCase):
#     pass


# class Icon_MaterModelTests(TestCase):
#     pass


# class Social_Network_ServiceModelTests(TestCase):
#     pass


# class AcknowledgmentsModelTests(TestCase):
#     pass


# class WorksModelTests(TestCase):
#     pass


# class Works_DetailModelTests(TestCase):
#     pass


# class Language_SkillsModelTests(TestCase):
#     pass


# class Library_SkillsModelTests(TestCase):
#     pass


# class DevOps_SkillsModelTests(TestCase):
#     pass


# class Work_Language_Skills_RelationShipModelTests(TestCase):
#     pass


# class Work_Library_Skills_RelationshipModelTests(TestCase):
#     pass


# class Work_DevOps_Skills_RelationshipModelTests(TestCase):
#     pass
