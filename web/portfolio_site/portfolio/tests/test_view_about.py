"""UT Test module for the About View."""
from django.test import TestCase
from django.urls import reverse

from . import utils

# Views Tests

class AboutViewTest(TestCase):
    """This class is an object to test the AboutView."""

    def test_no_profile(self):
        """If no profile resistered, the about page returns 404.
        """
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(response.status_code, 404)

    def test_no_sns(self):
        """If no sns are realted, the about page just returns profile.
        """
        profile = utils.create_profile()
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(response.context['profile'],profile)
        self.assertEqual(len(response.context['profile'].sns),0)

    def test_no_acknowledgment(self):
        """If no acknowledgment resistered, the about page just returns profile.
        """
        profile = utils.create_profile()
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(response.context['profile'],profile)
        self.assertEqual(len(response.context['acknowledgment']),0)

    def test_multi_profile(self):
        """If multiple profiles resistered, the about page returns the last profile.
        """
        utils.create_profile()
        profile = utils.create_another_profile()
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(response.context['profile'],profile)

    def test_multi_acknowledgment(self):
        """If multiple acknowledgment resistered, the about page returns all of them.
        """
        utils.create_profile()
        ack1 = utils.create_acknowledgment(True)
        ack2 = utils.create_acknowledgment(True)
        ack3 = utils.create_acknowledgment(True)
        response = self.client.get(reverse('portfolio:about'))
        self.assertQuerysetEqual(
            response.context['acknowledgment'],
            [ack1, ack2, ack3],
            ordered=False
        )
        self.assertEqual(response.context['acknowledgment'][0].comments, str(ack1))

    def test_unable_acknowledgment(self):
        """If disable acknowledgment resistered, the about page returns all except disable ones.
        """
        utils.create_profile()
        ack1 = utils.create_acknowledgment(True)
        utils.create_acknowledgment(False)
        ack3 = utils.create_acknowledgment(True)
        response = self.client.get(reverse('portfolio:about'))
        self.assertQuerysetEqual(
            response.context['acknowledgment'],
            [ack1, ack3],
            ordered=False
        )
