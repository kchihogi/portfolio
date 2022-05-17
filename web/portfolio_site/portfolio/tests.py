from django.test import TestCase
from django.urls import reverse
from portfolio.models import *
import datetime
from django.utils import timezone

# private methods
def _cretetProfile():
    prof = Profile(title = 'タイトル', subtitle = 'サブタイトル', first_name = 'ミカド', last_name = '赤城')
    prof.job = 'システムエンジニア'
    intro = ''
    for i in range(300):
        intro += str(i%10)
    prof.introduction = intro
    prof.face_photo = f'profile/face.png'
    prof.sub_photo = f'profile/sub.png'
    prof.save()
    return prof

def _createWork(work_name, private_work, start, end, sort=0, languages=[], libs=[], DevOps=[]):
    img = f'works/' + work_name + '.png'
    desc = ''
    for i in range(300):
        if i%10 == 0 and i !=0:
            desc += '\n'
        else:
            desc += 'Z'
    work = Work(title=work_name, image=img, private=private_work, description = desc, url='https://dummy_url', repository_url='https://dummy_repourl', sort=sort)
    work.save()

    desc = '詳細情報'
    work_detail = Work_Detail(Work_id=work.pk, sub_titile='サブタイトル', start_date=start, end_date=end, processes='工程A,工程B,工程C', detail_description= desc)
    work_detail.save()

    for record in Language_Skill.objects.all():
        for language in languages:
            if record.name == language:
                relation = Work_Language_Skill_RelationShip(Work_id=work.pk, Language_Skill_id=record.pk, sort=0)
                relation.save()

    for record in Library_Skill.objects.all():
        for lib in libs:
            if record.name == lib:
                relation = Work_Library_Skill_Relationship(Work_id=work.pk, Library_Skill_id=record.pk, sort=0)
                relation.save()

    for record in DevOps_Skill.objects.all():
        for dev in DevOps:
            if record.name == dev:
                relation = Work_DevOps_Skill_Relationship(Work_id=work.pk, DevOps_Skill_id=record.pk, sort=0)
                relation.save()
    return work

# Views Tests

class IndexViewTest(TestCase):
    def test_no_profile(self):
        """
        If no profile resistered, the index page returns 404.
        """
        response = self.client.get(reverse('portfolio:index'))
        self.assertEqual(response.status_code, 404)

    def test_no_work(self):
        """
        If no works, the index page contains "No works are available.".
        """
        profile = _cretetProfile()
        response = self.client.get(reverse('portfolio:index'))
        self.assertContains(response=response, text=profile.title)
        self.assertContains(response=response, text='No works are available.')
        self.assertQuerysetEqual(
            response.context['works'],
            [],
        )

    def test_three_no_private_works(self):
        """
        The index page shows three no private works.
        """
        _cretetProfile()
        private_work = 0
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c],
        )


    def test_six_no_private_works(self):
        """
        The index page shows six no private works.
        """
        _cretetProfile()
        private_work = 0
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=0)
        work_e = _createWork(work_name='WorkE', private_work=private_work, start=start, end=end,sort=0)
        work_f = _createWork(work_name='WorkF', private_work=private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )


    def test_seven_no_private_works(self):
        """
        The index page shows only six no private works, not seven works.
        """
        _cretetProfile()
        private_work = 0
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=0)
        work_e = _createWork(work_name='WorkE', private_work=private_work, start=start, end=end,sort=0)
        work_f = _createWork(work_name='WorkF', private_work=private_work, start=start, end=end,sort=0)
        _createWork(work_name='WorkG', private_work=private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )


    def test_three_private_works(self):
        """
        The index page shows three private works.
        """
        _cretetProfile()
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c],
        )


    def test_six_private_works(self):
        """
        The index page shows six private works.
        """
        _cretetProfile()
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=0)
        work_e = _createWork(work_name='WorkE', private_work=private_work, start=start, end=end,sort=0)
        work_f = _createWork(work_name='WorkF', private_work=private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )


    def test_seven_private_works(self):
        """
        The index page shows only six private works, not seven works.
        """
        _cretetProfile()
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=0)
        work_e = _createWork(work_name='WorkE', private_work=private_work, start=start, end=end,sort=0)
        work_f = _createWork(work_name='WorkF', private_work=private_work, start=start, end=end,sort=0)
        _createWork(work_name='WorkG', private_work=private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )


    def test_three_private_and_three_non_works(self):
        """
        The index page shows three no private works and three private works.
        """
        _cretetProfile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=non_private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=non_private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=0)
        work_e = _createWork(work_name='WorkE', private_work=non_private_work, start=start, end=end,sort=0)
        work_f = _createWork(work_name='WorkF', private_work=private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_two_private_and_two_non_works(self):
        """
        The index page shows two no private works and two private works.
        """
        _cretetProfile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=non_private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=non_private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d],
        )


    def test_two_private_and_five_non_works(self):
        """
        The index page shows four non private works and two private works.
        """
        _cretetProfile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=non_private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=non_private_work, start=start, end=end,sort=0)
        work_e = _createWork(work_name='WorkE', private_work=non_private_work, start=start, end=end,sort=0)
        work_f = _createWork(work_name='WorkF', private_work=non_private_work, start=start, end=end,sort=0)
        _createWork(work_name='WorkG', private_work=non_private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )


    def test_five_private_and_two_non_works(self):
        """
        The index page shows two non private works and four private works.
        """
        _cretetProfile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=0)
        _createWork(work_name='WorkE', private_work=private_work, start=start, end=end,sort=0)
        work_f = _createWork(work_name='WorkF', private_work=non_private_work, start=start, end=end,sort=0)
        work_g = _createWork(work_name='WorkG', private_work=non_private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_f, work_g],
        )


    def test_four_private_and_four_non_works(self):
        """
        The index page shows three non private works and three private works.
        """
        _cretetProfile()
        non_private_work = 0
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=0)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=0)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=0)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=0)
        work_e = _createWork(work_name='WorkE', private_work=non_private_work, start=start, end=end,sort=0)
        work_f = _createWork(work_name='WorkF', private_work=non_private_work, start=start, end=end,sort=0)
        work_g = _createWork(work_name='WorkG', private_work=non_private_work, start=start, end=end,sort=0)
        work_h = _createWork(work_name='WorkH', private_work=non_private_work, start=start, end=end,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_e, work_f, work_g],
        )


    def test_works_sorted(self):
        """
        This tests that works are sorted by the sort column. The value of the sort can be duplicated.
        """
        _cretetProfile()
        private_work = 0
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        work_a = _createWork(work_name='WorkA', private_work=private_work, start=start, end=end,sort=2)
        work_b = _createWork(work_name='WorkB', private_work=private_work, start=start, end=end,sort=1)
        work_c = _createWork(work_name='WorkC', private_work=private_work, start=start, end=end,sort=3)
        work_d = _createWork(work_name='WorkD', private_work=private_work, start=start, end=end,sort=2)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_b, work_a, work_d, work_c],
        )

# Models Tests

class ProfileModelTests(TestCase):
    _cretetProfile()


class Icon_MaterModelTests(TestCase):
    _cretetProfile()


class Social_Network_ServiceModelTests(TestCase):
    _cretetProfile()


class AcknowledgmentsModelTests(TestCase):
    _cretetProfile()


class WorksModelTests(TestCase):
    _cretetProfile()


class Works_DetailModelTests(TestCase):
    _cretetProfile()


class Language_SkillsModelTests(TestCase):
    _cretetProfile()


class Library_SkillsModelTests(TestCase):
    _cretetProfile()


class DevOps_SkillsModelTests(TestCase):
    _cretetProfile()


class Work_Language_Skills_RelationShipModelTests(TestCase):
    _cretetProfile()


class Work_Library_Skills_RelationshipModelTests(TestCase):
    _cretetProfile()


class Work_DevOps_Skills_RelationshipModelTests(TestCase):
    _cretetProfile()
