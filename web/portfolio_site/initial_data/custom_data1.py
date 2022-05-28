"""This module deletes and inserts test data into the DB.

You might execute master_data.py first.
"""
import datetime
from distutils import dir_util
import glob
import os

from django.utils import timezone

from portfolio_site import settings
from portfolio.models import Profile, Social_Network_Service, Icon_Mater, Acknowledgment
from portfolio.models import Language_Skill, Library_Skill, DevOps_Skill
from portfolio.models import Work, Work_Detail
from portfolio.models import Work_Language_Skill_RelationShip
from portfolio.models import Work_Library_Skill_Relationship
from portfolio.models import Work_DevOps_Skill_Relationship

from utils.cprint import ColorPrint as CP

def add_profile():
    """This copies media fiiles to the media root and inserts a profile record.
    """
    # mediaディレクトリの掃除
    prof_dir = settings.MEDIA_ROOT + '/profile'
    CP.print('Clena up media profile dir.('+ prof_dir +')',CP.GREEN)
    for file in glob.glob(prof_dir + '/**', recursive=True):
        if os.path.isfile(file):
            os.remove(file)
            CP.print('Deleted file.('+file+')',CP.YELLOW)

    # mediaを復元
    backup_media = 'initial_data/media/profile'
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
    prof.face_photo = 'profile/face.png'
    prof.sub_photo = 'profile/sub.png'
    prof.save()

    # DBにデータを追加
    CP.print('Add SNS records to DB.',CP.GREEN)
    for icon in Icon_Mater.objects.all():
        sns = Social_Network_Service()
        sns.Profile_id=prof.pk
        sns.name=icon.name
        sns.url='https://'+icon.name+'.com'
        sns.Icon_Mater_id=icon.pk
        sns.save()

def add_acknowledgment():
    """This inserts an acknowledgment.
    """
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

def add_language_skills():
    """This inserts language skills.
    """
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

def add_library_skills():
    """This inserts libraru skills.
    """
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

def add_dev_ops_skills():
    """This insets DevOps skills.
    """
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

def _create_work(work_name:str, private_work:int, start:datetime, end:datetime, sort:int=0):
    """This cretes work with foreign relations.

    Args:
        work_name (str): a name of work
        private_work (int): 0 for no private work. 1 for private work.
        start (datetime): start datetime when a project started.
        end (datetime): end datetime when a project ended.
        sort (int, optional): sort number to displaye the web page. Defaults to 0.

    Returns:
        Work: the model of Work created.
    """
    desc = ''
    for i in range(300):
        if i%10 == 0 and i !=0:
            desc += '\n'
        else:
            desc += 'Z'
    work = Work()
    work.title = work_name
    work.image='works/' + work_name + '.png'
    work.private=private_work
    work.description = desc
    work.url='https://dummy_url'
    work.repository_url='https://dummy_repourl'
    work.sort=sort
    work.save()

    work_detail = Work_Detail()
    work_detail.Work_id=work.pk
    work_detail.sub_titile='サブタイトル'
    work_detail.start_date=start
    work_detail.end_date=end
    work_detail.processes='工程A,工程B,工程C'
    work_detail.detail_description= '詳細情報'
    work_detail.save()
    return work

def _add_language_skills(work:Work, languages:list[str]):
    """This cretes relationship with work and language skills.

    Args:
        work (Work): the model of work.
        languages (list[str]): a list of language name.
    """
    if languages is not None:
        for record in Language_Skill.objects.all():
            for language in languages:
                if record.name == language:
                    relation = Work_Language_Skill_RelationShip()
                    relation.Work_id=work.pk
                    relation.Language_Skill_id=record.pk
                    relation.sort=0
                    relation.save()

def _add_lib_skills(work:Work, libs:list[str]):
    """This cretes relationship with work and libs skills.

    Args:
        work (Work): the model of work.
        libs (list[str]): a list of library name.
    """
    if libs is not None:
        for record in Library_Skill.objects.all():
            for lib in libs:
                if record.name == lib:
                    relation = Work_Library_Skill_Relationship()
                    relation.Work_id=work.pk
                    relation.Library_Skill_id=record.pk
                    relation.sort=0
                    relation.save()

def _add_dev_ops_skills(work:Work, dev_ops:list[str]):
    """This cretes relationship with work and dev_ops skills.

    Args:
        work (Work): the model of work.
        dev_ops (list[str]): a list of dev_ops skill name.
    """
    if dev_ops is not None:
        for record in DevOps_Skill.objects.all():
            for dev in dev_ops:
                if record.name == dev:
                    relation = Work_DevOps_Skill_Relationship()
                    relation.Work_id=work.pk
                    relation.DevOps_Skill_id=record.pk
                    relation.sort=0
                    relation.save()

def add_works():
    """This copies media files to media root and inserts records of work.
    """

    # mediaディレクトリの掃除
    work_dir = settings.MEDIA_ROOT + '/works'
    CP.print('Clena up media works dir.('+ work_dir +')',CP.GREEN)
    for file in glob.glob(work_dir + '/**', recursive=True):
        if os.path.isfile(file):
            os.remove(file)
            CP.print('Deleted file.('+file+')',CP.YELLOW)

    # mediaを復元
    backup_media = 'initial_data/media/works'
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
    dev_ops = ['Visual Studio','SQL Server Management Studio', 'Mysql Workbench' \
                ,'SVN', 'Git', 'A5 SQL Mk-2', 'Office', 'Redmine', 'JIRA', 'Jenkins', 'Teams']
    work = _create_work(work_name=work_name, private_work=private_work, start=start, end=end)
    _add_language_skills(work=work, languages=languages)
    _add_lib_skills(work=work,libs=libs)
    _add_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkB'
    private_work = 0
    start = timezone.now()
    languages = ['C++','Powershell']
    libs = ['F社標準ライブラリ']
    dev_ops = ['Visual Studio', 'Git', 'Office', 'Redmine', 'JIRA', 'Jenkins', 'Docker']
    work = _create_work(work_name=work_name, private_work=private_work, start=start, end=None)
    _add_language_skills(work=work, languages=languages)
    _add_lib_skills(work=work,libs=libs)
    _add_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkC'
    private_work = 0
    start = timezone.now() + datetime.timedelta(days=-365*2)
    end = timezone.now()
    languages = ['C#','Powershell','Java']
    libs = ['.Net Framework']
    dev_ops = ['Visual Studio','VS Code', 'Skype','SVN', 'Slack', 'Office']
    work = _create_work(work_name=work_name, private_work=private_work, start=start, end=end)
    _add_language_skills(work=work, languages=languages)
    _add_lib_skills(work=work,libs=libs)
    _add_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkD'
    private_work = 0
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = ['Python']
    libs = ['Django']
    dev_ops = ['VS Code', 'Git', 'Docker']
    work = _create_work(work_name=work_name, private_work=private_work, start=start, end=end)
    _add_language_skills(work=work, languages=languages)
    _add_lib_skills(work=work,libs=libs)
    _add_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkE'
    private_work = 1
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = []
    libs = []
    dev_ops = []
    work = _create_work(work_name=work_name, private_work=private_work, start=start, end=end)
    _add_language_skills(work=work, languages=languages)
    _add_lib_skills(work=work,libs=libs)
    _add_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkF'
    private_work = 1
    start = timezone.now()
    languages = ['C++','Powershell']
    libs = []
    dev_ops = ['Visual Studio', 'Git', 'Office', 'Redmine', 'JIRA', 'Jenkins', 'Docker']
    work = _create_work(work_name=work_name, private_work=private_work, start=start, end=None)
    _add_language_skills(work=work, languages=languages)
    _add_lib_skills(work=work,libs=libs)
    _add_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkG'
    private_work = 1
    start = timezone.now() + datetime.timedelta(days=-365*2)
    end = timezone.now()
    languages = ['C#','Powershell','Java']
    libs = ['.Net Framework']
    dev_ops = []
    work = _create_work(work_name=work_name, private_work=private_work, start=start, end=end)
    _add_language_skills(work=work, languages=languages)
    _add_lib_skills(work=work,libs=libs)
    _add_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkH'
    private_work = 1
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = []
    libs = ['Django']
    dev_ops = ['VS Code', 'Git', 'Docker']
    work = _create_work(work_name=work_name, private_work=private_work, start=start, end=end)
    _add_language_skills(work=work, languages=languages)
    _add_lib_skills(work=work,libs=libs)
    _add_dev_ops_skills(work=work,dev_ops=dev_ops)

    for i in range(300):
        work_name = f'WorkZZZ{str(i)}'
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        languages = ['Python']
        libs = ['Django']
        dev_ops = ['VS Code', 'Git', 'Docker']
        work = _create_work(work_name=work_name, private_work=private_work, start=start, end=end)
        _add_language_skills(work=work, languages=languages)
        _add_lib_skills(work=work,libs=libs)
        _add_dev_ops_skills(work=work,dev_ops=dev_ops)

add_profile()
add_acknowledgment()
add_language_skills()
add_library_skills()
add_dev_ops_skills()
add_works()
