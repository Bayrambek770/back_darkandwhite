from modeltranslation.translator import translator, TranslationOptions
from .models import Course


class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


translator.register(Course, CourseTranslationOptions)
