"""UT Test module for the modules of master data."""
import os

from django.test import TestCase

from initial_data import master_data
from portfolio_site import settings
from portfolio.models import Bcc, IconMater, MailSetting

class MasterDataTest(TestCase):
    """This class is an object to test the master data."""

    def test_add_icons(self):
        """Check exitsts of 4 files and 4records.
        """
        master_data.add_icon_master()
        master_data.add_icon_master()
        icon_dir = settings.MEDIA_ROOT + '/icons'
        self.assertTrue(os.path.isfile(icon_dir + '/Facebook.png'))
        self.assertTrue(os.path.isfile(icon_dir + '/Instagram.png'))
        self.assertTrue(os.path.isfile(icon_dir + '/LINE.png'))
        self.assertTrue(os.path.isfile(icon_dir + '/Twitter.png'))
        self.assertEqual(IconMater.objects.all().count(), 4)

    def test_add_mail_setting(self):
        """Check exitsts of one record.
        """
        master_data.add_mail_setting()
        master_data.add_mail_setting()
        self.assertEqual(MailSetting.objects.all().count(), 1)

    def test_add_bcc(self):
        """Check exitsts of 2records.
        """
        master_data.add_bcc()
        master_data.add_bcc()
        self.assertEqual(Bcc.objects.all().count(), 2)
