from django.db import models
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name = "Author")
    title = models.CharField(max_length = 50, verbose_name = "Title")
    summary = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Summary")
    slug = models.SlugField(max_length = 50)
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    article_image = models.FileField(blank = True , null = True, verbose_name="Image")
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete = models.CASCADE, verbose_name = "Comment", related_name="comments")
    comment_author = models.CharField(max_length = 50, verbose_name = "Author")
    comment_content = models.CharField(max_length = 200, verbose_name = "Content")
    comment_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date']
