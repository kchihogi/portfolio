"""UT Test module for the Contact View
"""
from django.core import mail
from django.test import override_settings, TestCase
from django.urls import reverse

from initial_data import master_data

class ContactViewTest(TestCase):
    """This class is an object to test the ContactView."""

    def test_no_main_setting_and_bcc(self):
        """If no MailSetting and BCC resistered, the maintenace page is returned.
        """
        response = self.client.get(reverse('portfolio:contact'))
        self.assertContains(response=response, text='Maintenance')

    def test_no_bcc(self):
        """If no BCC resistered, the maintenace page is returned.
        """
        master_data.add_mail_setting()
        master_data.add_mail_setting()
        response = self.client.get(reverse('portfolio:contact'))
        self.assertContains(response=response, text='Maintenance')

    def test_no_main_setting(self):
        """If no MailSetting resistered, the maintenace page is returned.
        """
        master_data.add_bcc()
        master_data.add_bcc()
        response = self.client.get(reverse('portfolio:contact'))
        self.assertContains(response=response, text='Maintenance')

    def test_contact_page(self):
        """If settings are properly resistered, the contact page is returned with 200.
        """
        master_data.add_mail_setting()
        master_data.add_bcc()
        response = self.client.get(reverse('portfolio:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response=response, text='Error:')

    def test_post_form_without_inputs(self):
        """If posting the contact form without inputs , it is returned with error info.
        """
        master_data.add_mail_setting()
        master_data.add_bcc()
        response = self.client.post(reverse('portfolio:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text='Error:')

    def test_post_form_with_inputs(self):
        """If posting the contact form, it is returned success page.
        """
        setting  = master_data.add_mail_setting()
        bcc = master_data.add_bcc()
        email = 'customer@dummy.email'
        customer='customer customer'
        subject = 'test subject'
        msg = 'test message'
        exp_subject = 'Thank you for your inquiry'
        exp_body = f'{customer}様\n\n※このメールは送信専用のメールアドレスから配信されています。\n'
        exp_body += 'ご返信いただいてもお答えできませんのでご了承ください。\n\nお問い合わせありがとうございます。\n'
        exp_body += 'お問い合わせを受け付けました。\n'
        exp_body += 'お問い合わせ内容の返答は、追ってご連絡させて頂きますので今しばらくお待ちください。\n\n'
        exp_body += 'お問い合わせ内容\n--------------------------------------------------\n'
        exp_body += f'【件名】: {subject}\n\n'
        exp_body += f'【本文】:\n{msg}\n'
        exp_body += '--------------------------------------------------\n'
        inputs = {'name':customer
                , 'email': email
                , 'subject':subject
                , 'message':msg}
        response = self.client.post(reverse('portfolio:contact'), inputs)
        self.assertRedirects(response
                            , reverse('portfolio:success')
                            , status_code=302
                            , target_status_code=200
                            , msg_prefix=exp_subject
                            , fetch_redirect_response=True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, setting.sender)
        self.assertEqual(mail.outbox[0].subject, '【自動返信】お問い合わせありがとうございます。')
        self.assertEqual(mail.outbox[0].to, [email])
        self.assertEqual(mail.outbox[0].bcc, bcc)
        self.assertEqual(mail.outbox[0].body, exp_body)

    def test_post_form_without_no_mailsettings(self):
        """If no MailSetting resistered and post form, the maintenace page is returned.
        """
        master_data.add_bcc()
        email = 'customer@dummy.email'
        customer='customer customer'
        subject = 'test subject'
        msg = 'test message'
        inputs = {'name':customer
                , 'email': email
                , 'subject':subject
                , 'message':msg}
        response = self.client.post(reverse('portfolio:contact'), inputs)
        self.assertContains(response=response, text='Maintenance')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_post_form_with_incorrect_mail_setting(self):
        """If an incorrect setting, it is returned contact page with error massage.
        """
        master_data.add_mail_setting()
        master_data.add_bcc()
        email = 'customer@dummy.email'
        customer='customer customer'
        subject = 'test subject'
        msg = 'test message'
        inputs = {'name':customer
                , 'email': email
                , 'subject':subject
                , 'message':msg}
        response = self.client.post(reverse('portfolio:contact'), inputs)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text='Error:')
