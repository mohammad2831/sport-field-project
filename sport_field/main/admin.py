from django import forms
from django.contrib import admin
from .models import Question, Answer, ResultUser

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        widgets = {
            'sport_points': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }



class AnswerInline(admin.TabularInline):
    """
    اینلاین برای نمایش و مدیریت گزینه‌های پاسخ (Answer) مرتبط با یک سوال.
    """
    model = Answer
    # form = AnswerForm # اگر AnswerForm را حذف می‌کنید، این خط را هم حذف کنید.
    extra = 1 # تعداد ردیف‌های خالی برای اضافه کردن پاسخ جدید در ابتدا
    min_num = 0 # حداقل تعداد فرم‌های اینلاین که باید وجود داشته باشد (0 یعنی می‌تواند خالی باشد)
    can_delete = True # اجازه حذف ردیف‌ها را می‌دهد.
    fields = ['text', 'points', 'age'] # فیلدهایی که در اینلاین نمایش داده می‌شوند.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['id', 'text', 'category', 'type']
    list_filter = ['category', 'type']
    search_fields = ['text']
    fields = ['text', 'category', 'type','max_age', 'min_age']

    def get_inline_instances(self, request, obj=None):
        if obj and obj.type != Question.CHOICE:
            return []
        return super().get_inline_instances(request, obj)




@admin.register(ResultUser)
class ResultUserAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست نمایش داده می‌شوند
    list_display = ('full_name', 'age', 'result', 'time')
    # فیلدهایی که قابل جستجو هستند
    search_fields = ('full_name', 'result')
    # فیلدهایی که می‌توان بر اساس آن‌ها فیلتر کرد
    list_filter = ('age', 'time')