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
        pass

    def test_six_no_private_works(self):
        """
        The index page shows six no private works.
        """
        pass

    def test_seven_no_private_works(self):
        """
        The index page shows only six no private works, not seven works.
        """
        pass

    def test_three_private_works(self):
        """
        The index page shows three private works.
        """
        pass

    def test_six_private_works(self):
        """
        The index page shows six private works.
        """
        pass

    def test_seven_private_works(self):
        """
        The index page shows only six private works, not seven works.
        """
        pass

    def test_three_private_and_three_non_works(self):
        """
        The index page shows three no private works and three private works.
        """
        pass

    def test_two_private_and_two_non_works(self):
        """
        The index page shows two no private works and two private works.
        """
        pass

    def test_two_private_and_five_non_works(self):
        """
        The index page shows four non private works and two private works.
        """
        pass

    def test_five_private_and_two_non_works(self):
        """
        The index page shows two non private works and four private works.
        """
        pass

    def test_four_private_and_four_non_works(self):
        """
        The index page shows three non private works and three private works.
        """
        pass

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
    pass

class Icon_MaterModelTests(TestCase):
    pass

class Social_Network_ServiceModelTests(TestCase):
    pass

class AcknowledgmentsModelTests(TestCase):
    pass

class WorksModelTests(TestCase):
    pass

class Works_DetailModelTests(TestCase):
    pass

class Language_SkillsModelTests(TestCase):
    pass

class Library_SkillsModelTests(TestCase):
    pass

class DevOps_SkillsModelTests(TestCase):
    pass

class Work_Language_Skills_RelationShipModelTests(TestCase):
    pass

class Work_Library_Skills_RelationshipModelTests(TestCase):
    pass

class Work_DevOps_Skills_RelationshipModelTests(TestCase):
    pass