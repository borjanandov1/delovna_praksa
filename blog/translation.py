from modeltranslation.translator import TranslationOptions, register

from .models import Category, Post


@register(Category)
class CategoryTR(TranslationOptions):
    fields = ("name",)


@register(Post)
class PostTR(TranslationOptions):
    fields = ("title", "excerpt", "body")
