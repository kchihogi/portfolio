"""This module deletes and inserts master data into the DB.
"""
from distutils import dir_util
import glob
import os
from pathlib import Path

from utils.cprint import ColorPrint as CP

from portfolio_site import settings
from portfolio.models import Bcc, IconMater, MailSetting

def add_icon_master():
    """This copies media files to media root and inserts records of icon master.
    """
    # mediaディレクトリの掃除
    icon_dir = settings.MEDIA_ROOT + '/icons'
    CP.print('Clena up media icon dir.('+ icon_dir +')',CP.GREEN)
    for file in glob.glob(icon_dir + '/**', recursive=True):
        if os.path.isfile(file):
            os.remove(file)
            CP.print('Deleted file.('+file+')',CP.YELLOW)

    # mediaを復元
    backup_media = str(Path(__file__).resolve().parent) + '/media/icons'
    CP.print('Copy media dir.(FROM:'+ backup_media + '  TO:'+ icon_dir +')',CP.GREEN)
    dir_util.copy_tree(backup_media, icon_dir)

    # DB データを全削除
    CP.print('Delete all DB Icon_Mater records.',CP.GREEN)
    for icon in IconMater.objects.all():
        CP.print('Deleted record.('+str(icon) +')',CP.YELLOW)
        icon.delete()

    # DBにデータを追加
    CP.print('Add Icon_Mater records to DB.',CP.GREEN)
    twitter = IconMater(name='Twitter', icon='icons/Twitter.png')
    twitter.save()
    facebook = IconMater(name='Facebook', icon='icons/Facebook.png')
    facebook.save()
    instagram = IconMater(name='Instagram', icon='icons/Instagram.png')
    instagram.save()
    line = IconMater(name='LINE', icon='icons/LINE.png')
    line.save()

def add_mail_setting():
    """This inserts records of mail setting.
    """
    # DB データを全削除
    for record in MailSetting.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    CP.print('Add MailSetting records to DB.',CP.GREEN)
    setting = MailSetting()
    setting.sender = 'example@hogehoge.com'
    setting.save()
    return setting

def add_bcc():
    """This inserts records of BCC.
    """
    # DB データを全削除
    for record in Bcc.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    CP.print('Add Bcc records to DB.',CP.GREEN)
    bcc1 = Bcc(email = 'example@hoghoge.com')
    bcc1.save()
    bcc2 = Bcc(email = 'example2@hoghoge.com')
    bcc2.save()
    return [bcc1, bcc2]
