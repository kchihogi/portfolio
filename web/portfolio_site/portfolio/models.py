from django.db import models

class Profile(models.Model):
    title = models.CharField('タイトル', max_length=100, null=False)
    subtitle = models.CharField('サブタイトル', max_length=100, null=False)
    first_name = models.CharField('名', max_length=100, null=False)
    last_name = models.CharField('氏', max_length=100, null=False)
    job = models.CharField('職業', max_length=100, null=True)
    introduction = models.CharField('自己紹介', max_length=300, null=True)
    face_photo = models.ImageField('顔写真', max_length=1024, null=True, blank=True, upload_to='profile')
    sub_photo = models.ImageField('サブ写真', max_length=1024, null=True, blank=True, upload_to='profile')

    def __str__(self):
        return self.title

class Icon_Mater(models.Model):
    name = models.CharField('名前', max_length=100, null=False)
    icon = models.ImageField('icon', max_length=1024, null=False, blank=True, upload_to='icons')

    def __str__(self):
        return self.name

class Social_Network_Service(models.Model):
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Profiles')
    name = models.CharField('名前', max_length=100, null=False)
    url = models.CharField('URL', max_length=1024, null=False)
    Icon_Mater = models.ForeignKey(Icon_Mater, on_delete=models.CASCADE, related_name='Icon_Maters')

    def __str__(self):
        return self.name

class Acknowledgment(models.Model):
    comments = models.TextField('コメント', null=True)
    enable = models.IntegerField('有効', null=True) #0:無効 1:有効 それ以外:有効

    def __str__(self):
        return self.comments

class Work(models.Model):
    title = models.CharField('タイトル', max_length=100, null=False)
    image = models.ImageField('メインビジュアル', max_length=1024, null=False, blank=True, upload_to='works')
    private = models.IntegerField('プライベート作品', null=False, default=0) #0:業務で作成, 1:プライベートで作成, それ以外:プライベートで作成
    description = models.CharField('概要', max_length=300, null=False)
    url = models.CharField('URL', max_length=1024, null=True)
    repository_url = models.CharField('リポジトリURL', max_length=1024, null=True)
    sort = models.IntegerField('順序', null=False)

    def __str__(self):
        return self.title

class Work_Detail(models.Model):
    Work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='Work_Details')
    sub_titile = models.CharField('サブタイトル', max_length=100, null=False)
    start_date = models.DateTimeField('制作開始', null=False)
    end_date = models.DateTimeField('制作終了', null=True)
    processes = models.CharField('担当工程', max_length=300, null=True)
    detail_description = models.TextField('詳細', null=True)

    def __str__(self):
        return self.sub_titile

class Language_Skill(models.Model):
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class Library_Skill(models.Model):
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class DevOps_Skill(models.Model):
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class Work_Language_Skill_RelationShip(models.Model):
    Work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='Lang_Works')
    Language_Skill = models.ForeignKey(Language_Skill, on_delete=models.CASCADE, related_name='Language_Skills')
    sort = models.IntegerField('順序', null=False, default=0)

class Work_Library_Skill_Relationship(models.Model):
    Work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='Lib_Works')
    Library_Skill = models.ForeignKey(Library_Skill, on_delete=models.CASCADE, related_name='Library_Skills')
    sort = models.IntegerField('順序', null=False, default=0)

class Work_DevOps_Skill_Relationship(models.Model):
    Work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='Dev_Works')
    DevOps_Skill = models.ForeignKey(DevOps_Skill, on_delete=models.CASCADE, related_name='DevOps_Skills')
    sort = models.IntegerField('順序', null=False, default=0)