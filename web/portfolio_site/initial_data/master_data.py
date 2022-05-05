from distutils import dir_util
import glob
import os
from portfolio.models import Icon_Mater
import portfolio_site.settings as settings
from utils.cprint import ColorPrint as CP

try:
    # mediaディレクトリの掃除
    CP.print('Clena up media dir.('+settings.MEDIA_ROOT+')',CP.BLUE)
    for file in glob.glob(settings.MEDIA_ROOT + '/**', recursive=True):
        if os.path.isfile(file):
            os.remove(file)
            CP.print('Deleted file.('+file+')',CP.YELLOW)

    # mediaを復元
    backup_media = f'initial_data/media'
    CP.print('Copy media dir.(FROM:'+ backup_media + '  TO:'+settings.MEDIA_ROOT+')',CP.BLUE)
    dir_util.copy_tree(backup_media, settings.MEDIA_ROOT)

    # DB データを全削除
    CP.print('Delete all DB records.',CP.BLUE)
    for icon in Icon_Mater.objects.all():
        CP.print('Deleted record.('+icon.__str__() +')',CP.YELLOW)
        icon.delete()

    # DBにデータを追加
    CP.print('Add records to DB.',CP.BLUE)
    Twitter = Icon_Mater(name='Twitter', icon=f'icons/Twitter.png')
    Twitter.save()

except Exception as e:
    CP.print('Exception occurs !!!',CP.RED)
    print(e)
except:
    CP.print('Unhandle Error !!!',CP.RED)