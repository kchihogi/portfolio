"""This module defines the structure of DB.
"""
from django.db import models

class Profile(models.Model):
    """The model of profile table.
    """
    sub='profile' #sub directory under the media.

    title = models.CharField('タイトル', max_length=100, null=False)
    subtitle = models.CharField('サブタイトル', max_length=100, null=False)
    first_name = models.CharField('名', max_length=100, null=False)
    last_name = models.CharField('氏', max_length=100, null=False)
    job = models.CharField('職業', max_length=100, null=True)
    introduction = models.CharField('自己紹介', max_length=300, null=True)
    face_photo = models.ImageField('顔写真', max_length=1024, null=True, blank=True, upload_to=sub)
    sub_photo = models.ImageField('サブ写真', max_length=1024, null=True, blank=True, upload_to=sub)

    def __str__(self):
        return self.title

class IconMater(models.Model):
    """The model of icon master table.
    """
    sub='icons' #sub directory under the media.

    name = models.CharField('名前', max_length=100, null=False)
    icon = models.ImageField('icon', max_length=1024, null=False, blank=True, upload_to=sub)

    def __str__(self):
        return self.name

class SocialNetworkService(models.Model):
    """The model of SNS table.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField('名前', max_length=100, null=False)
    url = models.CharField('URL', max_length=1024, null=False)
    icon_master = models.ForeignKey(IconMater, on_delete=models.CASCADE, related_name='icon_masters')

    def __str__(self):
        return self.name

class Acknowledgment(models.Model):
    """The model of acknowledgment table.
    """
    comments = models.TextField('コメント', null=True)
    enable = models.IntegerField('有効', null=True) #0:無効 1:有効 それ以外:有効

    def __str__(self):
        return self.comments

class Work(models.Model):
    """The model of work table.
    """
    sub='works' #sub directory under the media.

    title = models.CharField('タイトル', max_length=100, null=False)
    image = models.ImageField('メインビジュアル', max_length=1024, null=False, blank=True, upload_to=sub)
    #0:業務で作成, 1:プライベートで作成, それ以外:プライベートで作成
    private = models.IntegerField('プライベート作品', null=False, default=0)
    description = models.CharField('概要', max_length=300, null=False)
    url = models.CharField('URL', max_length=1024, null=True)
    repository_url = models.CharField('リポジトリURL', max_length=1024, null=True)
    sort = models.IntegerField('順序', null=False)

    def __str__(self):
        return self.title

class WorkDetail(models.Model):
    """The model of work detail table.
    """
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='work_details')
    sub_titile = models.CharField('サブタイトル', max_length=100, null=False)
    start_date = models.DateTimeField('制作開始', null=False)
    end_date = models.DateTimeField('制作終了', null=True)
    processes = models.CharField('担当工程', max_length=300, null=True)
    detail_description = models.TextField('詳細', null=True)

    def __str__(self):
        return self.sub_titile

class LanguageSkill(models.Model):
    """The model of language skill table.
    """
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class LibrarySkill(models.Model):
    """The model of library skill table.
    """
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class DevOpsSkill(models.Model):
    """The model of DevOps skill table.
    """
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class WorkLanguageSkillRelationShip(models.Model):
    """The model of the relationship table of work and language skills.
    """
    wrn = 'lang_works'
    lrn = 'language_skills'

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name=wrn)
    language_skill = models.ForeignKey(LanguageSkill, on_delete=models.CASCADE, related_name=lrn)
    sort = models.IntegerField('順序', null=False, default=0)

class WorkLibrarySkillRelationship(models.Model):
    """The model of the relationship table of work and library skills.
    """
    wrn = 'lib_works'
    lrn = 'library_skills'

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name=wrn)
    library_skill = models.ForeignKey(LibrarySkill, on_delete=models.CASCADE, related_name=lrn)
    sort = models.IntegerField('順序', null=False, default=0)

class WorkDevOpsSkillRelationship(models.Model):
    """The model of the relationship table of work and DevOps skills.
    """
    wrn = 'dev_works'
    lrn = 'dev_ops_skills'

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name=wrn)
    dev_ops_skill = models.ForeignKey(DevOpsSkill, on_delete=models.CASCADE, related_name=lrn)
    sort = models.IntegerField('順序', null=False, default=0)
