from django.contrib import admin

from .models import Article, Category, Comment

admin.site.register(Category)
admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date"]
    list_display_links = ["title", "created_date"]
    search_fields = ["title"]
    list_filter = ["created_date"]
    class Meta:
        model = Article

    def preview_content(self, article):
        return Truncator(article.content).chars(40, truncate='...')

    preview_content.short_description = 'Preview content'
    prepopulated_fields = {'slug': ('title', ), }
