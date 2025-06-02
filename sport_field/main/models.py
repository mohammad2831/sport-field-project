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
        default=CHOICE,  # پیش‌فرض سوالات چند گزینه‌ای هستند
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
        unique_together = ('question', 'text')

    def __str__(self):
        return f"{self.question.id} - {self.text} - {self.points}"
    





class UserResponse(models.Model):
    session_key = models.CharField(max_length=40, db_index=True, verbose_name="کلید سشن")
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name="سوال")
    # برای سوالات چند گزینه‌ای
    chosen_answer = models.ForeignKey(
        'Answer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="پاسخ انتخاب شده"
    )
    # برای سوالات متنی
    text_answer = models.TextField(null=True, blank=True, verbose_name="پاسخ متنی")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت پاسخ")

    class Meta:
        verbose_name = "پاسخ کاربر"
        verbose_name_plural = "پاسخ‌های کاربران"
        unique_together = ('session_key', 'question')

    def __str__(self):
        answer_text = self.chosen_answer.text if self.chosen_answer else self.text_answer
        return f"سشن {self.session_key[:10]}... - سوال: {self.question.id} - پاسخ: {answer_text[:50]}..."
    





class AnonymousUserProfile(models.Model):

    session_key = models.CharField(
        max_length=40,
        unique=True, # هر session_key فقط یک پروفایل را نشان می‌دهد.
        verbose_name="session key"
    )
    age = models.IntegerField(null=True, blank=True, verbose_name="سن")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد") # زمان ساخت رکورد
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی") # زمان آخرین بروزرسانی رکورد

    class Meta:
        verbose_name = "پروفایل کاربر ناشناس"
        verbose_name_plural = "پروفایل‌های کاربران ناشناس"

    def __str__(self):
        # نمایش خلاصه session_key برای خوانایی بیشتر در پنل ادمین و لاگ‌ها
        return f"پروفایل سشن: {self.session_key[:10]}..." if self.session_key else "پروفایل ناشناس"

