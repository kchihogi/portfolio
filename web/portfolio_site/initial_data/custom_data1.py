import datetime
from distutils import dir_util
from django.utils import timezone
import glob
import os
from portfolio.models import Profile, Social_Network_Service, Icon_Mater, Acknowledgment, Language_Skill, Library_Skill, DevOps_Skill, Work, Work_Detail, Work_Language_Skill_RelationShip ,Work_Library_Skill_Relationship, Work_DevOps_Skill_Relationship
import portfolio_site.settings as settings
from utils.cprint import ColorPrint as CP

def ProfileAdd():

    # mediaディレクトリの掃除
    prof_dir = settings.MEDIA_ROOT + '/profile'
    CP.print('Clena up media profile dir.('+ prof_dir +')',CP.GREEN)
    for file in glob.glob(prof_dir + '/**', recursive=True):
        if os.path.isfile(file):
            os.remove(file)
            CP.print('Deleted file.('+file+')',CP.YELLOW)

    # mediaを復元
    backup_media = f'initial_data/media/profile'
    CP.print('Copy media dir.(FROM:'+ backup_media + '  TO:'+ prof_dir +')',CP.GREEN)
    dir_util.copy_tree(backup_media, prof_dir)

    # DB データを全削除
    CP.print('Delete all DB SNS records.',CP.GREEN)
    for sns in Social_Network_Service.objects.all():
        CP.print('Deleted record.('+sns.__str__() +')',CP.YELLOW)
        sns.delete()

    # DB データを全削除
    CP.print('Delete all DB Profile records.',CP.GREEN)
    for prof in Profile.objects.all():
        CP.print('Deleted record.('+prof.__str__() +')',CP.YELLOW)
        prof.delete()

    # DBにデータを追加
    CP.print('Add Profile records to DB.',CP.GREEN)
    prof = Profile(title = 'タイトル', subtitle = 'サブタイトル', first_name = 'ミカド', last_name = '赤城')
    prof.job = 'システムエンジニア'
    intro = ''
    for i in range(300):
        intro += str(i%10)
    prof.introduction = intro
    prof.face_photo = f'profile/face.png'
    prof.sub_photo = f'profile/sub.png'
    prof.save()

    # DBにデータを追加
    CP.print('Add SNS records to DB.',CP.GREEN)
    for icon in Icon_Mater.objects.all():
        sns = Social_Network_Service(Profile_id=prof.pk, name=icon.name, url='https://'+icon.name+'.com', Icon_Mater_id=icon.pk)
        sns.save()

def AcknowledgmentAdd():
    # DB データを全削除
    CP.print('Delete all DB Acknowledgment records.',CP.GREEN)
    for ack in Acknowledgment.objects.all():
        CP.print('Deleted record.('+str(ack.pk) +')',CP.YELLOW)
        ack.delete()

    # DBにデータを追加
    CP.print('Add Acknowledgment records to DB.',CP.GREEN)
    cmts = ''
    for i in range(300):
        if i%10 == 0 and i !=0:
            cmts += '\n'
        cmts += 'X'
    ack = Acknowledgment(comments = cmts, enable = 1)
    ack.save()

def Language_SkillAdd():
    # DB データを全削除
    CP.print('Delete all DB Language_Skill records.',CP.GREEN)
    for record in Language_Skill.objects.all():
        CP.print('Deleted record.('+record.__str__() +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    CP.print('Add Language_Skill records to DB.',CP.GREEN)
    record = Language_Skill(name = 'C++', maturity = 5)
    record.save()
    record = Language_Skill(name = 'Python', maturity = 3)
    record.save()
    record = Language_Skill(name = 'C#', maturity = 2)
    record.save()
    record = Language_Skill(name = 'Powershell', maturity = 4)
    record.save()
    record = Language_Skill(name = 'PHP', maturity = 2)
    record.save()
    record = Language_Skill(name = 'Java', maturity = 1)
    record.save()
    record = Language_Skill(name = 'SQL(SQL Server, MySQL)', maturity = 5)
    record.save()

def Library_SkillAdd():
    # DB データを全削除
    CP.print('Delete all DB Library_Skill records.',CP.GREEN)
    for record in Library_Skill.objects.all():
        CP.print('Deleted record.('+record.__str__() +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    CP.print('Add Library_Skill records to DB.',CP.GREEN)
    record = Library_Skill(name = 'F社標準ライブラリ', maturity = 5)
    record.save()
    record = Library_Skill(name = 'Django', maturity = 2)
    record.save()
    record = Library_Skill(name = '.Net Framework', maturity = 2)
    record.save()

def DevOps_SkillAdd():
    # DB データを全削除
    CP.print('Delete all DB DevOps_Skill records.',CP.GREEN)
    for record in DevOps_Skill.objects.all():
        CP.print('Deleted record.('+record.__str__() +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    CP.print('Add DevOps_Skill records to DB.',CP.GREEN)
    record = DevOps_Skill(name = 'Visual Studio', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'VS Code', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'SQL Server Management Studio', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'Mysql Workbench', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'SVN', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'Git', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'A5 SQL Mk-2', maturity = 4)
    record.save()
    record = DevOps_Skill(name = 'Office', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'Redmine', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'JIRA', maturity = 4)
    record.save()
    record = DevOps_Skill(name = 'Jenkins', maturity = 5)
    record.save()
    record = DevOps_Skill(name = 'Teams', maturity = 4)
    record.save()
    record = DevOps_Skill(name = 'Skype', maturity = 4)
    record.save()
    record = DevOps_Skill(name = 'Zoom', maturity = 3)
    record.save()
    record = DevOps_Skill(name = 'Slack', maturity = 3)
    record.save()
    record = DevOps_Skill(name = 'Docker', maturity = 4)
    record.save()
    record = DevOps_Skill(name = 'myPHPAdmin', maturity = 2)
    record.save()

def _createWork(work_name, private_work, start, end, languages, libs, DevOps):
    CP.print('Add Work records to DB.('+work_name+')',CP.GREEN)
    img = f'works/' + work_name + '.png'
    desc = ''
    for i in range(300):
        if i%10 == 0 and i !=0:
            desc += '\n'
        else:
            desc += 'Z'
    work = Work(title=work_name, image=img, private=private_work, description = desc, url='https://dummy_url', repository_url='https://dummy_repourl', sort=0)
    work.save()

    desc = '詳細情報'
    work_detail = Work_Detail(Work_id=work.pk, sub_titile='サブタイトル', start_date=start, end_date=end, processes='工程A,工程B,工程C', detail_description= desc)
    work_detail.save()

    for record in Language_Skill.objects.all():
        for language in languages:
            if record.name == language:
                relation = Work_Language_Skill_RelationShip(Work_id=work.pk, Language_Skill_id=record.pk, sort=0)
                relation.save()

    for record in Library_Skill.objects.all():
        for lib in libs:
            if record.name == lib:
                relation = Work_Library_Skill_Relationship(Work_id=work.pk, Library_Skill_id=record.pk, sort=0)
                relation.save()

    for record in DevOps_Skill.objects.all():
        for dev in DevOps:
            if record.name == dev:
                relation = Work_DevOps_Skill_Relationship(Work_id=work.pk, DevOps_Skill_id=record.pk, sort=0)
                relation.save()

def WorkAdd():

    # mediaディレクトリの掃除
    work_dir = settings.MEDIA_ROOT + '/works'
    CP.print('Clena up media works dir.('+ work_dir +')',CP.GREEN)
    for file in glob.glob(work_dir + '/**', recursive=True):
        if os.path.isfile(file):
            os.remove(file)
            CP.print('Deleted file.('+file+')',CP.YELLOW)

    # mediaを復元
    backup_media = f'initial_data/media/works'
    CP.print('Copy media dir.(FROM:'+ backup_media + '  TO:'+ work_dir +')',CP.GREEN)
    dir_util.copy_tree(backup_media, work_dir)

    # DB データを全削除
    CP.print('Delete all DB Work_DevOps_Skill_Relationship records.',CP.GREEN)
    for record in Work_DevOps_Skill_Relationship.objects.all():
        CP.print('Deleted record.('+record.__str__() +')',CP.YELLOW)
        record.delete()

    # DB データを全削除
    CP.print('Delete all DB Work_Library_Skill_Relationship records.',CP.GREEN)
    for record in Work_Library_Skill_Relationship.objects.all():
        CP.print('Deleted record.('+record.__str__() +')',CP.YELLOW)
        record.delete()

    # DB データを全削除
    CP.print('Delete all DB Work_Language_Skill_RelationShip records.',CP.GREEN)
    for record in Work_Language_Skill_RelationShip.objects.all():
        CP.print('Deleted record.('+record.__str__() +')',CP.YELLOW)
        record.delete()

    # DB データを全削除
    CP.print('Delete all DB Work_Detail records.',CP.GREEN)
    for record in Work_Detail.objects.all():
        CP.print('Deleted record.('+record.__str__() +')',CP.YELLOW)
        record.delete()

    # DB データを全削除
    CP.print('Delete all DB Work records.',CP.GREEN)
    for record in Work.objects.all():
        CP.print('Deleted record.('+record.__str__() +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    work_name = 'WorkA'
    private_work = 0
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = ['C++','SQL(SQL Server, MySQL)','Powershell','PHP']
    libs = ['F社標準ライブラリ']
    DevOps = ['Visual Studio','SQL Server Management Studio', 'Mysql Workbench','SVN', 'Git', 'A5 SQL Mk-2', 'Office', 'Redmine', 'JIRA', 'Jenkins', 'Teams']
    _createWork(work_name=work_name, private_work=private_work, start=start, end=end,languages=languages,libs=libs,DevOps=DevOps)
    
    work_name = 'WorkB'
    private_work = 0
    start = timezone.now()
    languages = ['C++','Powershell']
    libs = ['F社標準ライブラリ']
    DevOps = ['Visual Studio', 'Git', 'Office', 'Redmine', 'JIRA', 'Jenkins', 'Docker']
    _createWork(work_name=work_name, private_work=private_work, start=start, end=None,languages=languages,libs=libs,DevOps=DevOps)
    
    work_name = 'WorkC'
    private_work = 0
    start = timezone.now() + datetime.timedelta(days=-365*2)
    end = timezone.now()
    languages = ['C#','Powershell','Java']
    libs = ['.Net Framework']
    DevOps = ['Visual Studio','VS Code', 'Skype','SVN', 'Slack', 'Office']
    _createWork(work_name=work_name, private_work=private_work, start=start, end=end,languages=languages,libs=libs,DevOps=DevOps)
    
    work_name = 'WorkD'
    private_work = 0
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = ['Python']
    libs = ['Django']
    DevOps = ['VS Code', 'Git', 'Docker']
    _createWork(work_name=work_name, private_work=private_work, start=start, end=end,languages=languages,libs=libs,DevOps=DevOps)
    
    work_name = 'WorkE'
    private_work = 1
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = []
    libs = []
    DevOps = []
    _createWork(work_name=work_name, private_work=private_work, start=start, end=end,languages=languages,libs=libs,DevOps=DevOps)
    
    work_name = 'WorkF'
    private_work = 1
    start = timezone.now()
    languages = ['C++','Powershell']
    libs = []
    DevOps = ['Visual Studio', 'Git', 'Office', 'Redmine', 'JIRA', 'Jenkins', 'Docker']
    _createWork(work_name=work_name, private_work=private_work, start=start, end=None,languages=languages,libs=libs,DevOps=DevOps)
    
    work_name = 'WorkG'
    private_work = 1
    start = timezone.now() + datetime.timedelta(days=-365*2)
    end = timezone.now()
    languages = ['C#','Powershell','Java']
    libs = ['.Net Framework']
    DevOps = []
    _createWork(work_name=work_name, private_work=private_work, start=start, end=end,languages=languages,libs=libs,DevOps=DevOps)
    
    work_name = 'WorkH'
    private_work = 1
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = []
    libs = ['Django']
    DevOps = ['VS Code', 'Git', 'Docker']
    _createWork(work_name=work_name, private_work=private_work, start=start, end=end,languages=languages,libs=libs,DevOps=DevOps)

try:
    ProfileAdd()
    AcknowledgmentAdd()
    Language_SkillAdd()
    Library_SkillAdd()
    DevOps_SkillAdd()
    WorkAdd()
except Exception as e:
    CP.print('Exception occurs !!!',CP.RED)
    print(e)
except:
    CP.print('Unhandle Error !!!',CP.RED)