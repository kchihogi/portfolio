"""This module deletes and inserts test data into the DB.

You might execute master_data.py first.
"""
import datetime
from distutils import dir_util
import glob
import os
from pathlib import Path
from typing import Tuple

from django.utils import timezone

from utils.cprint import ColorPrint as CP

from portfolio_site import settings
from portfolio.models import Profile, SocialNetworkService, IconMater, Acknowledgment
from portfolio.models import LanguageSkill, LibrarySkill, DevOpsSkill
from portfolio.models import Work, WorkDetail
from portfolio.models import WorkLanguageSkillRelationShip
from portfolio.models import WorkLibrarySkillRelationship
from portfolio.models import WorkDevOpsSkillRelationship

def create_profile():
    """This cretes fixed profile.

    Returns:
        Profile: the model of Profile created.
    """
    prof = Profile(title = 'タイトル', subtitle = 'サブタイトル', first_name = 'ミカド', last_name = '赤城')
    prof.job = 'システムエンジニア'
    intro = ''
    for i in range(300):
        intro += str(i%10)
    prof.introduction = intro
    prof.face_photo = 'profile/face.png'
    prof.sub_photo = 'profile/sub.png'
    prof.save()
    return prof

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
    backup_media =str(Path(__file__).resolve().parent) + '/media/profile'
    CP.print('Copy media dir.(FROM:'+ backup_media + '  TO:'+ prof_dir +')',CP.GREEN)
    dir_util.copy_tree(backup_media, prof_dir)

    # DB データを全削除
    CP.print('Delete all DB SNS records.',CP.GREEN)
    for sns in SocialNetworkService.objects.all():
        CP.print('Deleted record.('+str(sns) +')',CP.YELLOW)
        sns.delete()

    # DB データを全削除
    CP.print('Delete all DB Profile records.',CP.GREEN)
    for prof in Profile.objects.all():
        CP.print('Deleted record.('+str(prof) +')',CP.YELLOW)
        prof.delete()

    # DBにデータを追加
    CP.print('Add Profile records to DB.',CP.GREEN)
    prof = create_profile()

    # DBにデータを追加
    CP.print('Add SNS records to DB.',CP.GREEN)
    for icon in IconMater.objects.all():
        sns = SocialNetworkService()
        sns.profile_id=prof.pk
        sns.name=icon.name
        sns.url='https://'+icon.name+'.com'
        sns.icon_master_id=icon.pk
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
    CP.print('Delete all DB LanguageSkill records.',CP.GREEN)
    for record in LanguageSkill.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    CP.print('Add LanguageSkill records to DB.',CP.GREEN)
    record = LanguageSkill(name = 'C++', maturity = 5)
    record.save()
    record = LanguageSkill(name = 'Python', maturity = 3)
    record.save()
    record = LanguageSkill(name = 'C#', maturity = 2)
    record.save()
    record = LanguageSkill(name = 'Powershell', maturity = 4)
    record.save()
    record = LanguageSkill(name = 'PHP', maturity = 2)
    record.save()
    record = LanguageSkill(name = 'Java', maturity = 1)
    record.save()
    record = LanguageSkill(name = 'SQL(SQL Server, MySQL)', maturity = 5)
    record.save()

def add_library_skills():
    """This inserts libraru skills.
    """
    # DB データを全削除
    CP.print('Delete all DB LibrarySkill records.',CP.GREEN)
    for record in LibrarySkill.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    CP.print('Add LibrarySkill records to DB.',CP.GREEN)
    record = LibrarySkill(name = 'F社標準ライブラリ', maturity = 5)
    record.save()
    record = LibrarySkill(name = 'Django', maturity = 2)
    record.save()
    record = LibrarySkill(name = '.Net Framework', maturity = 2)
    record.save()

def add_dev_ops_skills():
    """This insets DevOps skills.
    """
    # DB データを全削除
    CP.print('Delete all DB DevOpsSkill records.',CP.GREEN)
    for record in DevOpsSkill.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DBにデータを追加
    CP.print('Add DevOpsSkill records to DB.',CP.GREEN)
    record = DevOpsSkill(name = 'Visual Studio', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'VS Code', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'SQL Server Management Studio', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'Mysql Workbench', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'SVN', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'Git', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'A5 SQL Mk-2', maturity = 4)
    record.save()
    record = DevOpsSkill(name = 'Office', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'Redmine', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'JIRA', maturity = 4)
    record.save()
    record = DevOpsSkill(name = 'Jenkins', maturity = 5)
    record.save()
    record = DevOpsSkill(name = 'Teams', maturity = 4)
    record.save()
    record = DevOpsSkill(name = 'Skype', maturity = 4)
    record.save()
    record = DevOpsSkill(name = 'Zoom', maturity = 3)
    record.save()
    record = DevOpsSkill(name = 'Slack', maturity = 3)
    record.save()
    record = DevOpsSkill(name = 'Docker', maturity = 4)
    record.save()
    record = DevOpsSkill(name = 'myPHPAdmin', maturity = 2)
    record.save()

def create_work(work_name:str, private_work:int, sort:int=0):
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
    return work

def relate_work_detail(work:Work, proc:str, start:datetime, end:datetime, desc:str):
    """This creates relationship with work and work detail.

    Args:
        work (Work): the model of work.
        start (datetime): start datetime when a project started.
        end (datetime): end datetime when a project ended.
        desc (str): Description of the work detail.

    Returns:
        Work_Detail: the model of Work_Detail created.
    """
    work_detail = WorkDetail()
    work_detail.work_id=work.pk
    work_detail.sub_titile=f'{work.title} SubTitle'
    work_detail.start_date=start
    work_detail.end_date=end
    work_detail.processes=proc
    work_detail.detail_description= desc
    work_detail.save()
    return work_detail

def relate_language_skills(work:Work, languages:list[Tuple[str,int]]):
    """This cretes relationship with work and language skills.

    Args:
        work (Work): the model of work.
        languages (list[Tuple[str,int]]): a list of language name and sort number.
    """
    if languages is not None:
        for record in LanguageSkill.objects.all():
            for language in languages:
                if record.name == language[0]:
                    relation = WorkLanguageSkillRelationShip()
                    relation.work_id=work.pk
                    relation.language_skill_id=record.pk
                    relation.sort=language[1]
                    relation.save()

def relate_lib_skills(work:Work, libs:list[Tuple[str,int]]):
    """This cretes relationship with work and libs skills.

    Args:
        work (Work): the model of work.
        libs (list[Tuple[str,int]]): a list of library name and sort number.
    """
    if libs is not None:
        for record in LibrarySkill.objects.all():
            for lib in libs:
                if record.name == lib[0]:
                    relation = WorkLibrarySkillRelationship()
                    relation.work_id=work.pk
                    relation.library_skill_id=record.pk
                    relation.sort=lib[1]
                    relation.save()

def relate_dev_ops_skills(work:Work, dev_ops:list[Tuple[str,int]]):
    """This cretes relationship with work and dev_ops skills.

    Args:
        work (Work): the model of work.
        dev_ops (list[Tuple[str,int]]): a list of dev_ops skill name and sort number.
    """
    if dev_ops is not None:
        for record in DevOpsSkill.objects.all():
            for dev in dev_ops:
                if record.name == dev[0]:
                    relation = WorkDevOpsSkillRelationship()
                    relation.work_id=work.pk
                    relation.dev_ops_skill_id=record.pk
                    relation.sort=dev[1]
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
    backup_media = str(Path(__file__).resolve().parent) + '/media/works'
    CP.print('Copy media dir.(FROM:'+ backup_media + '  TO:'+ work_dir +')',CP.GREEN)
    dir_util.copy_tree(backup_media, work_dir)

    _delete_works()

    _add_non_private_works()

    _add_private_works()

    _add_works(300)

def _delete_works():
    """This deletes records of work.
    """

    # DB データを全削除
    CP.print('Delete all DB WorkDevOpsSkillRelationship records.',CP.GREEN)
    for record in WorkDevOpsSkillRelationship.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DB データを全削除
    CP.print('Delete all DB WorkLibrarySkillRelationship records.',CP.GREEN)
    for record in WorkLibrarySkillRelationship.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DB データを全削除
    CP.print('Delete all DB WorkLanguageSkillRelationShip records.',CP.GREEN)
    for record in WorkLanguageSkillRelationShip.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DB データを全削除
    CP.print('Delete all DB Work_Detail records.',CP.GREEN)
    for record in WorkDetail.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

    # DB データを全削除
    CP.print('Delete all DB Work records.',CP.GREEN)
    for record in Work.objects.all():
        CP.print('Deleted record.('+str(record) +')',CP.YELLOW)
        record.delete()

def _add_works(num:int):
    """This adds works by for-loop.

    Args:
        num (int): number of works to add.
    """
    desc=''
    for i in range(num):
        work_name = f'WorkZZZ{str(i)}'
        private_work = 1
        start = timezone.now() + datetime.timedelta(days=-365)
        end = timezone.now()
        languages = [('Python',0)]
        libs = [('Django',0)]
        dev_ops = [('VS Code',0), ('Git',0), ('Docker',0)]
        work = create_work(work_name=work_name, private_work=private_work)
        proc='工程A,工程B,工程C'
        desc+=f'詳細情報{i}'
        relate_work_detail(work,proc,start,end,desc)
        relate_language_skills(work=work, languages=languages)
        relate_lib_skills(work=work,libs=libs)
        relate_dev_ops_skills(work=work,dev_ops=dev_ops)

def _add_non_private_works():
    """This adds records of non private works.
    """
    private_work = 0
    proc='工程A,工程B,工程C'
    desc='詳細情報'

    # DBにデータを追加
    work_name = 'WorkA'
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = [('C++',0),('SQL(SQL Server, MySQL)'),('Powershell',0),('PHP',0)]
    libs = [('F社標準ライブラリ',0)]
    dev_ops = [('Visual Studio',0),('SQL Server Management Studio', 0), ('Mysql Workbench',0) \
                ,('SVN',0), ('Git',0), ('A5 SQL Mk-2',0), ('Office', 0), ('Redmine',0) \
                , ('JIRA',0), ('Jenkins', 0), ('Teams',0)]
    work = create_work(work_name=work_name, private_work=private_work)
    relate_work_detail(work,proc,start,end,desc)
    relate_language_skills(work=work, languages=languages)
    relate_lib_skills(work=work,libs=libs)
    relate_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkB'
    start = timezone.now()
    languages = [('C++', 0),('Powershell',0)]
    libs = [('F社標準ライブラリ', 0)]
    dev_ops = [('Visual Studio',0), ('Git',0), ('Office',0), ('Redmine',0) \
                , ('JIRA',0), ('Jenkins',0), ('Docker', 0)]
    work = create_work(work_name=work_name, private_work=private_work)
    relate_work_detail(work,proc,start,None,desc)
    relate_language_skills(work=work, languages=languages)
    relate_lib_skills(work=work,libs=libs)
    relate_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkC'
    start = timezone.now() + datetime.timedelta(days=-365*2)
    end = timezone.now()
    languages = [('C#',0),('Powershell',0),('Java',0)]
    libs = [('.Net Framework',0)]
    dev_ops = [('Visual Studio',0),('VS Code',0), ('Skype',0),('SVN',0), ('Slack',0), ('Office',0)]
    work = create_work(work_name=work_name, private_work=private_work)
    relate_work_detail(work,proc,start,end,desc)
    relate_language_skills(work=work, languages=languages)
    relate_lib_skills(work=work,libs=libs)
    relate_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkD'
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = [('Python', 0)]
    libs = [('Django', 0)]
    dev_ops = [('VS Code',0), ('Git',0), ('Docker',0)]
    work = create_work(work_name=work_name, private_work=private_work)
    relate_work_detail(work,proc,start,end,desc)
    relate_language_skills(work=work, languages=languages)
    relate_lib_skills(work=work,libs=libs)
    relate_dev_ops_skills(work=work,dev_ops=dev_ops)

def _add_private_works():
    """This adds records of private works
    """
    private_work = 1
    proc='工程A,工程B,工程C'
    desc='詳細情報'

    work_name = 'WorkE'
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = []
    libs = []
    dev_ops = []
    work = create_work(work_name=work_name, private_work=private_work)

    relate_work_detail(work,proc,start,end,desc)
    relate_language_skills(work=work, languages=languages)
    relate_lib_skills(work=work,libs=libs)
    relate_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkF'
    start = timezone.now()
    languages = [('C++',0),('Powershell', 0)]
    libs = []
    dev_ops = [('Visual Studio', 0), ('Git', 0), ('Office', 0) \
                , ('Redmine',0), ('JIRA', 0), ('Jenkins', 0), ('Docker',0)]
    work = create_work(work_name=work_name, private_work=private_work)
    relate_work_detail(work,proc,start,None,desc)
    relate_language_skills(work=work, languages=languages)
    relate_lib_skills(work=work,libs=libs)
    relate_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkG'
    start = timezone.now() + datetime.timedelta(days=-365*2)
    end = timezone.now()
    languages = [('C#',0),('Powershell', 0),('Java', 0)]
    libs = [('.Net Framework', 0)]
    dev_ops = []
    work = create_work(work_name=work_name, private_work=private_work)
    relate_work_detail(work,proc,start,end,desc)
    relate_language_skills(work=work, languages=languages)
    relate_lib_skills(work=work,libs=libs)
    relate_dev_ops_skills(work=work,dev_ops=dev_ops)

    work_name = 'WorkH'
    start = timezone.now() + datetime.timedelta(days=-365)
    end = timezone.now()
    languages = []
    libs = [('Django', 0)]
    dev_ops = [('VS Code', 0), ('Git', 0), ('Docker', 0)]
    work = create_work(work_name=work_name, private_work=private_work)
    relate_work_detail(work,proc,start,end,desc)
    relate_language_skills(work=work, languages=languages)
    relate_lib_skills(work=work,libs=libs)
    relate_dev_ops_skills(work=work,dev_ops=dev_ops)
