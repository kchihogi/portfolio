from django.db import models

class Profile(models.Model):
    title = models.CharField('タイトル', max_length=100, null=False)
    subtitle = models.CharField('サブタイトル', max_length=100, null=False)
    first_name = models.CharField('名', max_length=100, null=False)
    last_name = models.CharField('氏', max_length=100, null=False)
    job = models.CharField('職業', max_length=100, null=True)
    introduction = models.CharField('自己紹介', max_length=300, null=True)
    face_photo = models.CharField('顔写真', max_length=1024, null=True)
    sub_photo = models.CharField('サブ写真', max_length=1024, null=True)

    def __str__(self):
        return self.title

class Icon_Mater(models.Model):
    icon = models.CharField('icon', max_length=1024, null=False)

    def __str__(self):
        return self.icon

class Social_Network_Service(models.Model):
    Profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField('名前', max_length=100, null=False)
    url = models.CharField('URL', max_length=1024, null=False)
    Icon_id = models.ForeignKey(Icon_Mater, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Acknowledgments(models.Model):
    comments = models.TextField('コメント', null=True)
    enable = models.IntegerField('有効', null=True) #0:無効 1:有効 それ以外:有効

    def __str__(self):
        return self.comments

class Works(models.Model):
    title = models.CharField('タイトル', max_length=100, null=False)
    image = models.CharField('メインビジュアル', max_length=1024, null=False)
    private = models.IntegerField('プライベート作品', null=False, default=0) #0:業務で作成, 1:プライベートで作成, それ以外:プライベートで作成
    description = models.CharField('概要', max_length=300, null=False)
    url = models.CharField('URL', max_length=1024, null=True)
    repository_url = models.CharField('リポジトリURL', max_length=1024, null=True)
    sort = models.IntegerField('順序', null=False)

    def __str__(self):
        return self.title

class Works_Detail(models.Model):
    Work_id = models.ForeignKey(Works, on_delete=models.CASCADE)
    sub_titile = models.CharField('サブタイトル', max_length=100, null=False)
    start_date = models.DateTimeField('制作開始', null=False)
    end_date = models.DateTimeField('制作終了', null=True)
    processes = models.CharField('担当工程', max_length=300, null=True)
    detail_description = models.TextField('詳細', null=True)

    def __str__(self):
        return self.sub_titile

class Language_Skills(models.Model):
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class Library_Skills(models.Model):
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class DevOps_Skills(models.Model):
    name = models.CharField('名前', max_length=100, null=False)
    maturity = models.IntegerField('成熟度', null=True) #5段階評価

    def __str__(self):
        return self.name

class Work_Language_Skills_RelationShip(models.Model):
    Work_id = models.ForeignKey(Works, on_delete=models.CASCADE)
    Language_Skills_id = models.ForeignKey(Language_Skills, on_delete=models.CASCADE)
    sort = models.IntegerField('順序', null=False, default=0)

class Work_Library_Skills_Relationship(models.Model):
    Work_id = models.ForeignKey(Works, on_delete=models.CASCADE)
    Library_Skill_id = models.ForeignKey(Library_Skills, on_delete=models.CASCADE)
    sort = models.IntegerField('順序', null=False, default=0)

class Work_DevOps_Skills_Relationship(models.Model):
    Work_id = models.ForeignKey(Works, on_delete=models.CASCADE)
    DevOps_Skill_id = models.ForeignKey(DevOps_Skills, on_delete=models.CASCADE)
    sort = models.IntegerField('順序', null=False, default=0)