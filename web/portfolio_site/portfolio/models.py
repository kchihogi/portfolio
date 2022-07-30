"""This module defines the structure of DB.
"""
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    """The model of profile table.
    """
    sub='profile' #sub directory under the media.

    title = models.CharField('タイトル', max_length=100, null=False)
    subtitle = models.CharField('サブタイトル', max_length=100, null=False)
    first_name = models.CharField('名', max_length=100, null=False)
    last_name = models.CharField('氏', max_length=100, null=False)
    job = models.CharField('職業', max_length=100, null=True, blank=True)
    face_photo = models.ImageField('顔写真', max_length=1024, null=True, blank=True, upload_to=sub)
    sub_photo = models.ImageField('サブ写真', max_length=1024, null=True, blank=True, upload_to=sub)

    def __str__(self):
        return self.title

class ProfileDetail(models.Model):
    """The model of ProfileDetail table.
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    introduction = models.CharField('自己紹介', max_length=300, null=True)
    gender = models.CharField('性別', max_length=100, null=True, blank=True)
    birthday = models.DateField('生年月日', null=True, blank=True)
    email = models.EmailField('メールアドレス', max_length=240, null=True, blank=True)
    phone = PhoneNumberField('電話番号', null=True, blank=True)
    address = models.CharField('住所', max_length=300, null=True, blank=True)

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
    prn = 'profiles'
    irn = 'icon_masters'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name=prn)
    name = models.CharField('名前', max_length=100, null=False)
    url = models.CharField('URL', max_length=1024, null=False)
    icon_master = models.ForeignKey(IconMater, on_delete=models.CASCADE, related_name=irn)

    def __str__(self):
        return self.name

class Acknowledgment(models.Model):
    """The model of acknowledgment table.
    """
    comments = models.TextField('コメント', null=True, blank=True)
    enable = models.IntegerField('有効', null=True, blank=True) #0:無効 1:有効 それ以外:有効

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
    url = models.CharField('URL', max_length=1024, null=True, blank=True)
    repository_url = models.CharField('リポジトリURL', max_length=1024, null=True, blank=True)
    sort = models.IntegerField('順序', null=False)

    def __str__(self):
        return self.title

class WorkDetail(models.Model):
    """The model of work detail table.
    """
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='work_details')
    sub_titile = models.CharField('サブタイトル', max_length=100, null=False)
    start_date = models.DateField('制作開始', null=False)
    end_date = models.DateField('制作終了', null=True, blank=True)
    processes = models.CharField('担当工程', max_length=300, null=True, blank=True)
    detail_description = models.TextField('詳細', null=True, blank=True)

    def __str__(self):
        return self.sub_titile

class LanguageSkill(models.Model):
    """The model of language skill table.
    """
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True, blank=True) #5段階評価

    def __str__(self):
        return self.name

class LibrarySkill(models.Model):
    """The model of library skill table.
    """
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True, blank=True) #5段階評価

    def __str__(self):
        return self.name

class DevOpsSkill(models.Model):
    """The model of DevOps skill table.
    """
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True, blank=True) #5段階評価

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

class Customer(models.Model):
    """The model of customer table.
    """
    name = models.CharField('お客様氏名', null=False, blank=False, max_length=100)
    email = models.EmailField('お客様メールアドレス', null=False, blank=False, unique=True)
    newsletter = models.BooleanField('メルマガ希望', null=False, blank=False, default=True)
    valid = models.BooleanField('有効', null=False, blank= False, default=True)
    reject = models.BooleanField('拒否', null=False, blank=False, default=False)
    count = models.IntegerField('問い合わせ回数', null=False, blank=False, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
        ]

    def __str__(self):
        return self.name

class Contact(models.Model):
    """The model of contact table.
    """
    name = models.CharField('お客様氏名', null=False, blank=False, max_length=100)
    email = models.EmailField('お客様メールアドレス', null=False, blank=False)
    subject = models.CharField('件名', null=False, blank=False, max_length=256)
    message = models.TextField('本文', null=False, blank=False)
    time = models.DateTimeField('送信日時', null=False, blank=True)

    def __str__(self):
        return self.email

class Bcc(models.Model):
    """The model of BCC table.
    """
    email = models.EmailField('担当者メールアドレス', null=False, blank=False)
    name = models.CharField('担当者氏名', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.email

class MailSetting(models.Model):
    """The model of mail setting table.
    """
    sender = models.EmailField('送信メールアドレス', null=False, blank=False)
    enable = models.BooleanField('有効', null=False, blank=False, default=True)

    def __str__(self):
        return self.sender
