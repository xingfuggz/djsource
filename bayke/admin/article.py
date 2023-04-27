from django.contrib import admin

from bayke.admin.base import BaseModelAdmin
from bayke.models.article import BaykeArticleCategory, BaykeArticle, BaykeArticleTag


@admin.register(BaykeArticleCategory)
class BaykeArticleCategoryAdmin(BaseModelAdmin):
    '''Admin View for BaykeArticleCategory'''

    list_display = ('name', 'icon', 'desc', 'add_date')
    search_fields = ('name', 'desc')


@admin.register(BaykeArticle)
class BaykeArticleAdmin(BaseModelAdmin):
    '''Admin View for BaykeArticleCategory'''

    list_display = ('title', 'category', 'add_date')
    search_fields = ('title', 'desc')
    
    def save_model(self, request, obj, form, change) -> None:
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
    
admin.site.register(BaykeArticleTag)