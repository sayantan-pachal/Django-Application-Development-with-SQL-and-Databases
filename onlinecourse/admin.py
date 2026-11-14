from django.contrib import admin
# Exactly seven imported classes in total from .models as required:
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


# Inline class to display choices inside the Question admin page
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# Inline class to display questions inside the Course admin page
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


# Inline class to display lessons inside the Course admin page
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 2


# Admin configuration for Question model
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'course', 'grade')
    search_fields = ('question_text',)
    list_filter = ('course',)


# Admin configuration for Lesson model
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    search_fields = ('title', 'content')
    list_filter = ('course',)


# Admin configuration for Course model
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date', 'total_enrollment')
    search_fields = ('name', 'description')
    list_filter = ('pub_date',)


# Register models so that the "Online Course" section appears on Django Admin
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
