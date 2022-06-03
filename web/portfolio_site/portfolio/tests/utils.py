"""Utils for UT tests."""
import datetime
from operator import itemgetter
from typing import Tuple

from ..models import Profile, Work, WorkDetail
from ..models import LanguageSkill, WorkLanguageSkillRelationShip
from ..models import LibrarySkill, WorkLibrarySkillRelationship
from ..models import DevOpsSkill, WorkDevOpsSkillRelationship

def cretet_profile():
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

def create_work(work_name:str, private_work:int, sort:int=0):
    """This cretes work with foreign relations.

    Args:
        work_name (str): a name of work
        private_work (int): 0 for no private work. 1 for private work.
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

def relate_work_detail(work:Work, sub:str, proc:str, start:datetime, end:datetime, desc:str):
    """This creates relationship with work and work detail.

    Args:
        work (Work): the model of work.
        sub (str): Subtitle
        proc (str): Processes. Comma separated value.
        start (datetime): start datetime when a project started.
        end (datetime): end datetime when a project ended.
        desc (str): Description of the work detail.

    Returns:
        Work_Detail: the model of Work_Detail created.
    """
    work_detail = WorkDetail()
    work_detail.work_id=work.pk
    work_detail.sub_titile=sub
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

def add_language_skills():
    """This inserts language skills.
    """
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
    record = LibrarySkill(name = 'F社標準ライブラリ', maturity = 5)
    record.save()
    record = LibrarySkill(name = 'Django', maturity = 2)
    record.save()
    record = LibrarySkill(name = '.Net Framework', maturity = 2)
    record.save()

def add_dev_ops_skills():
    """This insets DevOps skills.
    """
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

def assert_skills(
    works:list[Work],
    attr:str,
    col1:str,
    col2:str,
    skillsset:list[list[Tuple[str,int]]]
    ):
    """This compares works to skills. If that does not match, it raises the AssertionError.

    Args:
        works (list[Work]): A list of works.
        attr (str): A table name, or an alias of a table naem, witch realated to a work for skills.
        col1 (str): A column name of the table which you set in the attr argument.
        This compares to the first column of one of the skills argument.
        col2 (str): A column name of the table which you set in the attr argument.
        This compares to the second column of one of the skills argument.
        skillsset (list[list[Tuple[str,int]]]): A list of skills to be expected.

    Raises:
        AssertionError: Works do not match skills.
        TypeError: col1 has to be <table>.<field> separated with ".".
    """
    if len(col1.split(".")) != 2:
        raise TypeError('col1 has to be <table>.<field> separated with ".".')

    if len(works) != len(skillsset):
        msg = "works conut are equal to skillslist."
        raise AssertionError(msg)

    for (work, skills) in zip(works, skillsset):
        sorted_skills = sorted(skills, key=itemgetter(1))
        match = True

        result_str = '['
        if len(getattr(work, attr)) != len(sorted_skills):
            match = False
            if len(getattr(work, attr)) == 0:
                result_str += ', '
        for (ret, exp) in zip(getattr(work, attr), sorted_skills):
            skill_name = getattr(getattr(ret, col1.split(".")[0]), col1.split(".")[1])
            sort_num = getattr(ret, col2)
            if skill_name != exp[0] or sort_num != exp[1]:
                match = False
                break
        if not match:
            for ret in getattr(work, attr):
                skill_name = getattr(getattr(ret, col1.split(".")[0]), col1.split(".")[1])
                sort_num = getattr(ret, col2)
                result_str += f"('{skill_name}', {str(sort_num)}), "
            result_str = f'{result_str[:-2]}]'
            msg = f'{work.__str__()} {str(type(work))}\n\n'
            msg += f'expected:{sorted_skills}\n\n'
            msg += f'result:{result_str}\n'
            raise AssertionError(msg)
