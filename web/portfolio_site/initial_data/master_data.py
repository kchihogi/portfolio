from distutils import dir_util
import glob
import os
from portfolio.models import Icon_Mater
import portfolio_site.settings as settings
from utils.cprint import ColorPrint as CP

def IconMaster():
    # mediaディレクトリの掃除
    icon_dir = settings.MEDIA_ROOT + '/icons'
    CP.print('Clena up media icon dir.('+ icon_dir +')',CP.GREEN)
    for file in glob.glob(icon_dir + '/**', recursive=True):
        if os.path.isfile(file):
            os.remove(file)
            CP.print('Deleted file.('+file+')',CP.YELLOW)

    # mediaを復元
    backup_media = f'initial_data/media/icons'
    CP.print('Copy media dir.(FROM:'+ backup_media + '  TO:'+ icon_dir +')',CP.GREEN)
    dir_util.copy_tree(backup_media, icon_dir)

    # DB データを全削除
    CP.print('Delete all DB Icon_Mater records.',CP.GREEN)
    for icon in Icon_Mater.objects.all():
        CP.print('Deleted record.('+icon.__str__() +')',CP.YELLOW)
        icon.delete()

    # DBにデータを追加
    CP.print('Add Icon_Mater records to DB.',CP.GREEN)
    Twitter = Icon_Mater(name='Twitter', icon=f'icons/Twitter.png')
    Twitter.save()
    Facebook = Icon_Mater(name='Facebook', icon=f'icons/Facebook.png')
    Facebook.save()
    Instagram = Icon_Mater(name='Instagram', icon=f'icons/Instagram.png')
    Instagram.save()
    LINE = Icon_Mater(name='LINE', icon=f'icons/LINE.png')
    LINE.save()

try:
    IconMaster()
except Exception as e:
    CP.print('Exception occurs !!!',CP.RED)
    print(e)
except:
    CP.print('Unhandle Error !!!',CP.RED)