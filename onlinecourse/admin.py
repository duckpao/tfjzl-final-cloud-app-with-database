from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# Cấu hình giao diện chỉnh sửa lồng nhau (Inline)
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# Cấu hình hiển thị trang quản trị Admin
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course', 'grade']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']

# Đăng ký chính xác 7 model vào Admin Site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)