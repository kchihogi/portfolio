"""UT Test module for the modules of custom data utils."""
import os

from django.test import TestCase

from initial_data import custom_data_utils, master_data
from portfolio_site import settings
from portfolio.models import Acknowledgment, DevOpsSkill, LanguageSkill, LibrarySkill, Profile, Work

class CustomDataTest(TestCase):
    """This class is an object to test the custom data utils."""

    def test_add_profile(self):
        """Check exitsts of 2 files and 1record.
        """
        master_data.add_icon_master()
        custom_data_utils.add_profile()
        custom_data_utils.add_profile()
        profile_dir = settings.MEDIA_ROOT + '/profile'
        self.assertTrue(os.path.isfile(profile_dir + '/face.png'))
        self.assertTrue(os.path.isfile(profile_dir + '/sub.png'))
        self.assertEqual(Profile.objects.all().count(), 1)

    def test_add_acknowledgment(self):
        """Check exitsts of 1record.
        """
        custom_data_utils.add_acknowledgment()
        custom_data_utils.add_acknowledgment()
        self.assertEqual(Acknowledgment.objects.all().count(), 1)

    def test_add_language_skills(self):
        """Check exitsts of 7records.
        """
        custom_data_utils.add_language_skills()
        custom_data_utils.add_language_skills()
        self.assertEqual(LanguageSkill.objects.all().count(), 7)

    def test_add_library_skills(self):
        """Check exitsts of 3records.
        """
        custom_data_utils.add_library_skills()
        custom_data_utils.add_library_skills()
        self.assertEqual(LibrarySkill.objects.all().count(), 3)

    def test_add_dev_ops_skills(self):
        """Check exitsts of 17records.
        """
        custom_data_utils.add_dev_ops_skills()
        custom_data_utils.add_dev_ops_skills()
        self.assertEqual(DevOpsSkill.objects.all().count(), 17)

    def test_add_works(self):
        """Check exitsts of 8files and 308records.
        """
        custom_data_utils.add_language_skills()
        custom_data_utils.add_library_skills()
        custom_data_utils.add_dev_ops_skills()
        custom_data_utils.add_works()
        custom_data_utils.add_works()
        work_dir = settings.MEDIA_ROOT + '/works'
        self.assertTrue(os.path.isfile(work_dir + '/WorkA.png'))
        self.assertTrue(os.path.isfile(work_dir + '/WorkB.png'))
        self.assertTrue(os.path.isfile(work_dir + '/WorkC.png'))
        self.assertTrue(os.path.isfile(work_dir + '/WorkD.png'))
        self.assertTrue(os.path.isfile(work_dir + '/WorkE.png'))
        self.assertTrue(os.path.isfile(work_dir + '/WorkF.png'))
        self.assertTrue(os.path.isfile(work_dir + '/WorkG.png'))
        self.assertTrue(os.path.isfile(work_dir + '/WorkH.png'))
        self.assertEqual(Work.objects.all().count(), 308)
