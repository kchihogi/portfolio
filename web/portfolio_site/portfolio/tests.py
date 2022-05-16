from urllib import response
from django.test import TestCase
from django.urls import reverse

# Views Tests

class IndexViewTest(TestCase):
    def test_no_profile(self):
        response = self.client.get(reverse('portfolio:index'))
        self.assertEqual(response.status_code, 404)

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