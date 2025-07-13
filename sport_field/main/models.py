from django.db import models

class SportFields(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name="name-sport")
    description = models.TextField(blank=True, null=True, verbose_name="description")

    class Meta:
        verbose_name = "name-sport"
        verbose_name_plural = "name-sports"

    def __str__(self):
        return self.name
    


class Question(models.Model):
    TEXT = 'text'
    CHOICE = 'choice'
    QUESTION_TYPES = [
        (TEXT, 'متنی'),
        (CHOICE, 'چند گزینه ای'),
    ]

    text = models.TextField(verbose_name="متن سوال")
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    category = models.CharField(max_length=50, verbose_name="دسته بندی")
    type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default=CHOICE, 
        verbose_name="نوع سوال"
    )

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوالات"
        ordering = ['id']

    def __str__(self):
        return f"{self.id} - {self.text[:50]}... ({self.get_type_display()})"

class Answer(models.Model):
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="سوال"
    )
    text = models.CharField(max_length=200, verbose_name="متن پاسخ")
    points = models.IntegerField(default=0, verbose_name="امتیاز") 
    age= models.IntegerField(default=0, verbose_name="age")

    class Meta:
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ‌ها"

    def __str__(self):
        return f"{self.question.id} - {self.text} - {self.points}"
    





class UserCategoryScore(models.Model):

    session_key = models.ForeignKey( 
        'AnonymousUserProfile', 
        on_delete=models.CASCADE, 
        to_field='session_key',
        db_index=True,
        verbose_name="سشن کاربر ناشناس"
    )
    category = models.CharField(max_length=50,verbose_name="دسته بندی سوال")
    score = models.FloatField(default=0,verbose_name="امتیاز کسب شده در این دسته بندی")

    class Meta:
        verbose_name = "امتیاز دسته بندی کاربر"
        verbose_name_plural = "امتیازات دسته بندی کاربران"
        unique_together = ('session_key', 'category')

    def __str__(self):
        return f"سشن {self.session_key[:10]}... - دسته: {self.category} - امتیاز: {self.score}"






class AnonymousUserProfile(models.Model):
    full_name = models.CharField(max_length=200, unique=False,default='Anonymous User')
    session_key = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="session key"
    )
    age = models.IntegerField(null=True, blank=True, verbose_name="سن")

    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد") 
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی") 

    class Meta:
        verbose_name = "پروفایل کاربر ناشناس"
        verbose_name_plural = "پروفایل‌های کاربران ناشناس"

    def __str__(self):
        return f"پروفایل سشن: {self.session_key[:10]}..." if self.session_key else "پروفایل ناشناس"

class ResultUser(models.Model):
    full_name = models.TextField(max_length=200,unique=False)
    age = models.IntegerField(default=0)
    result = models.TextField(max_length=250, unique=False)
    time = models.TimeField()