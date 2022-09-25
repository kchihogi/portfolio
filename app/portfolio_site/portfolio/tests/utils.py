"""Utils for UT tests."""
import datetime
from operator import itemgetter
from typing import Tuple

from initial_data import custom_data_utils

from ..models import Profile, Work

def create_profile():
    """This creates fixed profile.

    Returns:
        Profile: the model of Profile created.
    """
    return custom_data_utils.create_profile()

def create_another_profile():
    """This creates fixed profile.

    Returns:
        Profile: the model of Profile created.
    """
    return custom_data_utils.create_another_profile()

def create_profile_detail(profile:Profile):
    """This creates fixed profile detail.

    Args:
        profile (Profile): the model of Profile, which is parent.

    Returns:
        ProfileDetail: the model of ProfileDetail created.
    """
    return custom_data_utils.create_profile_detail(profile)

def create_work(work_name:str, private_work:int, sort:int=0):
    """This creates work with foreign relations.

    Args:
        work_name (str): a name of work
        private_work (int): 0 for no private work. 1 for private work.
        sort (int, optional): sort number to displaye the web page. Defaults to 0.

    Returns:
        Work: the model of Work created.
    """
    return custom_data_utils.create_work(work_name, private_work, sort)

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
    return custom_data_utils.relate_work_detail(work,proc,start,end,desc)

def relate_language_skills(work:Work, languages:list[Tuple[str,int]]):
    """This creates relationship with work and language skills.

    Args:
        work (Work): the model of work.
        languages (list[Tuple[str,int]]): a list of language name and sort number.
    """
    custom_data_utils.relate_language_skills(work,languages)

def relate_lib_skills(work:Work, libs:list[Tuple[str,int]]):
    """This creates relationship with work and libs skills.

    Args:
        work (Work): the model of work.
        libs (list[Tuple[str,int]]): a list of library name and sort number.
    """
    custom_data_utils.relate_lib_skills(work, libs)

def relate_dev_ops_skills(work:Work, dev_ops:list[Tuple[str,int]]):
    """This creates relationship with work and dev_ops skills.

    Args:
        work (Work): the model of work.
        dev_ops (list[Tuple[str,int]]): a list of dev_ops skill name and sort number.
    """
    custom_data_utils.relate_dev_ops_skills(work, dev_ops)

def add_language_skills():
    """This inserts language skills.
    """
    custom_data_utils.add_language_skills()

def add_library_skills():
    """This inserts library skills.
    """
    custom_data_utils.add_library_skills()

def add_dev_ops_skills():
    """This insets DevOps skills.
    """
    custom_data_utils.add_dev_ops_skills()

def create_language_skills(name:str, maturity:int):
    """This inserts language skills.

    Args:
        name (str): name
        maturity (int): maturity(1-5, or None)

    Returns:
        LanguageSkill: the model of LanguageSkill created.
    """
    return custom_data_utils.create_language_skills(name, maturity)

def create_library_skills(name:str, maturity:int):
    """This inserts library skills.

    Args:
        name (str): name
        maturity (int): maturity(1-5, or None)

    Returns:
        LibrarySkill: the model of LibrarySkill created.
    """
    return custom_data_utils.create_library_skills(name, maturity)

def create_dev_ops_skills(name:str, maturity:int):
    """This inserts DevOps skills.

    Args:
        name (str): name
        maturity (int): maturity(1-5, or None)

    Returns:
        DevOpsSkill: the model of DevOpsSkill created.
    """
    return custom_data_utils.create_dev_ops_skills(name, maturity)

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
            msg = f'{str(work)} {str(type(work))}\n\n'
            msg += f'expected:{sorted_skills}\n\n'
            msg += f'result:{result_str}\n'
            raise AssertionError(msg)

def assert_skills_set(
    works:list[Work],
    langskillsset:list[list[Tuple[str,int]]],
    libskillsset:list[list[Tuple[str,int]]],
    devskillsset:list[list[Tuple[str,int]]]):
    """This repeats assert_skills for language, library, and DevOps skills.
    """
    assert_skills(
        works,
        "lang_details",
        "language_skill.name",
        "sort",
        langskillsset,
    )

    assert_skills(
        works,
        "lib_details",
        "library_skill.name",
        "sort",
        libskillsset,
    )

    assert_skills(
        works,
        "dev_details",
        "dev_ops_skill.name",
        "sort",
        devskillsset,
    )

def create_personal_base():
    """This inserts profile, language skills, library skills, and DevOps skills.
    """
    create_profile()
    add_language_skills()
    add_library_skills()
    add_dev_ops_skills()

def create_acknowledgment(enable:bool):
    """This inserts an acknowledgment.

    Args:
        enable (bool): enable

    Returns:
        Acknowledgment: the model of Acknowledgment created.
    """
    return custom_data_utils.create_acknowledgment(enable)
