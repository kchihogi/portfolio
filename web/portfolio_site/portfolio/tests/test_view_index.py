"""UT Test module for the Index View."""
from django.test import TestCase
from django.urls import reverse

from . import utils

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
        profile = utils.cretet_profile()
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
        utils.cretet_profile()
        private_work = 0
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c],
        )

    def test_six_no_private_works(self):
        """The index page shows six no private works.
        """
        utils.cretet_profile()
        private_work = 0
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        work_d = utils.create_work('WorkD', private_work,sort=0)
        work_e = utils.create_work('WorkE', private_work,sort=0)
        work_f = utils.create_work('WorkF', private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_seven_no_private_works(self):
        """The index page shows only six no private works, not seven works.
        """
        utils.cretet_profile()
        private_work = 0
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        work_d = utils.create_work('WorkD', private_work,sort=0)
        work_e = utils.create_work('WorkE', private_work,sort=0)
        work_f = utils.create_work('WorkF', private_work,sort=0)
        utils.create_work('WorkG', private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_three_private_works(self):
        """The index page shows three private works.
        """
        utils.cretet_profile()
        private_work = 1
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c],
        )

    def test_six_private_works(self):
        """The index page shows six private works.
        """
        utils.cretet_profile()
        private_work = 1
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        work_d = utils.create_work('WorkD', private_work,sort=0)
        work_e = utils.create_work('WorkE', private_work,sort=0)
        work_f = utils.create_work('WorkF', private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_seven_private_works(self):
        """The index page shows only six private works, not seven works.
        """
        utils.cretet_profile()
        private_work = 1
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        work_d = utils.create_work('WorkD', private_work,sort=0)
        work_e = utils.create_work('WorkE', private_work,sort=0)
        work_f = utils.create_work('WorkF', private_work,sort=0)
        utils.create_work('WorkG', private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_b, work_c, work_d, work_e, work_f],
        )

    def test_three_private_and_three_non_works(self):
        """The index page shows three no private works and three private works.
        """
        utils.cretet_profile()
        non_private_work = 0
        private_work = 1
        work_a = utils.create_work('WorkA', non_private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', non_private_work,sort=0)
        work_d = utils.create_work('WorkD', private_work,sort=0)
        work_e = utils.create_work('WorkE', non_private_work,sort=0)
        work_f = utils.create_work('WorkF', private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_c, work_e, work_b, work_d, work_f],
        )

    def test_two_private_and_two_non_works(self):
        """The index page shows two no private works and two private works.
        """
        utils.cretet_profile()
        non_private_work = 0
        private_work = 1
        work_a = utils.create_work('WorkA', non_private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', non_private_work,sort=0)
        work_d = utils.create_work('WorkD', private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_a, work_c, work_b, work_d],
        )

    def test_two_private_and_five_non_works(self):
        """The index page shows four non private works and two private works.
        """
        utils.cretet_profile()
        non_private_work = 0
        private_work = 1
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', non_private_work,sort=0)
        work_d = utils.create_work('WorkD', non_private_work,sort=0)
        work_e = utils.create_work('WorkE', non_private_work,sort=0)
        work_f = utils.create_work('WorkF', non_private_work,sort=0)
        utils.create_work('WorkG', non_private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_c, work_d, work_e, work_f, work_a, work_b],
        )

    def test_five_private_and_two_non_works(self):
        """The index page shows two non private works and four private works.
        """
        utils.cretet_profile()
        non_private_work = 0
        private_work = 1
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        work_d = utils.create_work('WorkD', private_work,sort=0)
        utils.create_work('WorkE', private_work,sort=0)
        work_f = utils.create_work('WorkF', non_private_work,sort=0)
        work_g = utils.create_work('WorkG', non_private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_f, work_g, work_a, work_b, work_c, work_d],
        )

    def test_four_private_and_four_non_works(self):
        """The index page shows three non private works and three private works.
        """
        utils.cretet_profile()
        non_private_work = 0
        private_work = 1
        work_a = utils.create_work('WorkA', private_work,sort=0)
        work_b = utils.create_work('WorkB', private_work,sort=0)
        work_c = utils.create_work('WorkC', private_work,sort=0)
        utils.create_work('WorkD', private_work,sort=0)
        work_e = utils.create_work('WorkE', non_private_work,sort=0)
        work_f = utils.create_work('WorkF', non_private_work,sort=0)
        work_g = utils.create_work('WorkG', non_private_work,sort=0)
        utils.create_work('WorkH', non_private_work,sort=0)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_e, work_f, work_g, work_a, work_b, work_c],
        )

    def test_works_sorted(self):
        """This tests that works are sorted by the sort column.

        The value of the sort can be duplicated.
        """
        utils.cretet_profile()
        private_work = 0
        work_a = utils.create_work('WorkA', private_work,sort=2)
        work_b = utils.create_work('WorkB', private_work,sort=1)
        work_c = utils.create_work('WorkC', private_work,sort=3)
        work_d = utils.create_work('WorkD', private_work,sort=2)
        response = self.client.get(reverse('portfolio:index'))
        self.assertQuerysetEqual(
            response.context['works'],
            [work_b, work_a, work_d, work_c],
        )
