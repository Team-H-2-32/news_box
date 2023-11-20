from modeltranslation.translator import register, TranslationOptions
from .models import News
from main.models import Category

@register(News)
class NewsTranslationOption(TranslationOptions):
    fields = ('title', 'description')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category', )

