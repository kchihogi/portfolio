from portfolio.models import Profile
from utils.cprint import ColorPrint as CP

def ProfileAdd():
    # DB データを全削除
    CP.print('Delete all DB Profile records.',CP.GREEN)
    for prof in Profile.objects.all():
        CP.print('Deleted record.('+prof.__str__() +')',CP.YELLOW)
        prof.delete()

    # DBにデータを追加
    CP.print('Add Profile records to DB.',CP.GREEN)
    prof = Profile(title = 'タイトル', subtitle = 'サブタイトル', first_name = 'ミカド', last_name = '赤城')
    prof.save()

try:
    ProfileAdd()
except Exception as e:
    CP.print('Exception occurs !!!',CP.RED)
    print(e)
except:
    CP.print('Unhandle Error !!!',CP.RED)