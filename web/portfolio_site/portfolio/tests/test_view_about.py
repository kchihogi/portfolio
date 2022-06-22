"""UT Test module for the About View."""
from django.test import TestCase
from django.utils import timezone
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

    def test_no_language_skills(self):
        """If no lang resistered, the about page just returns profile.
        """
        utils.create_profile()
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(len(response.context['lang']),0)

    def test_no_library_skills(self):
        """If no lib resistered, the about page just returns profile.
        """
        utils.create_profile()
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(len(response.context['lib']),0)

    def test_no_dev_ops_skills(self):
        """If no dev resistered, the about page just returns profile.
        """
        utils.create_profile()
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(len(response.context['dev']),0)

    def test_multi_language_skills(self):
        """If multiple lang resistered, the about page returns all of them.
        """
        utils.create_profile()
        lang1 = utils.create_language_skills('C#',1)
        lang2 = utils.create_language_skills('C++',3)
        lang3 = utils.create_language_skills('Python',5)
        lang4 = utils.create_language_skills('Powershell',None)
        response = self.client.get(reverse('portfolio:about'))
        self.assertQuerysetEqual(
            response.context['lang'],
            [lang3, lang2, lang1, lang4],
        )

    def test_multi_library_skills(self):
        """If multiple lib resistered, the about page returns all of them.
        """
        utils.create_profile()
        lib1 = utils.create_library_skills('lib1',None)
        lib2 = utils.create_library_skills('lib2',3)
        lib3 = utils.create_library_skills('lib3',2)
        lib4 = utils.create_library_skills('lib4',1)
        response = self.client.get(reverse('portfolio:about'))
        self.assertQuerysetEqual(
            response.context['lib'],
            [lib2, lib3, lib4, lib1],
        )

    def test_multi_dev_ops_skills(self):
        """If multiple dev resistered, the about page returns all of them.
        """
        utils.create_profile()
        dev1 = utils.create_dev_ops_skills('DevOps1',None)
        dev2 = utils.create_dev_ops_skills('DevOps',1)
        dev3 = utils.create_dev_ops_skills('DevOps3',None)
        dev4 = utils.create_dev_ops_skills('DevOps',2)
        response = self.client.get(reverse('portfolio:about'))
        self.assertQuerysetEqual(
            response.context['dev'],
            [dev4, dev2, dev1, dev3],
        )

    def test_profile_with_extra_info(self):
        """Test if profile returns   gender,birthday,email,phone,address
        """
        profile = utils.create_profile()
        profile.gender = 'male'
        profile.birthday = timezone.now()
        profile.email = 'example@hogehoge.com'
        profile.phone = '08012345678'
        profile.address = '2-8-1 Nishishinjuku,Shinjuku, Tokyo 163-8001 Japan'
        profile = utils.update_profile(profile)
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(response.context['profile'],profile)
