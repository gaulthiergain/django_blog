from django import forms
from .models import Article, Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "summary", "content", "category", "article_image"]

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label = "name")
    class Meta:
        model = Category
        fields = ["name"]

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label='', widget= forms.TextInput(attrs={'placeholder':'Your email'}))
    subject = forms.CharField(required=True, label='', widget= forms.TextInput(attrs={'placeholder':'Your subject'}))
    message = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder':'Your message'}))
    class Meta:
        fields = [""]
