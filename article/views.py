from django.shortcuts import render, HttpResponse, redirect, get_object_or_404,reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CategoryForm, ContactForm
from .models import Article, Category, Comment
from decouple import config

def articles(request):
    NB_articles = 3 # Show 3 articles per page
    keyword = request.GET.get("keyword")
    keyword_cat = request.GET.get("category")
    keyword_date = request.GET.get("date")
    categories = Category.objects.all()

    if keyword:
        article_list = Article.objects.filter(title__contains = keyword)
        paginator = Paginator(article_list, NB_articles)
        page = request.GET.get('page')
        articles = paginator.get_page(page)
        return render(request,"articles.html", {"articles":articles, "categories": categories})

    if keyword_cat:
        article_list = Article.objects.filter(category__name__contains = keyword_cat)
        paginator = Paginator(article_list, NB_articles)
        page = request.GET.get('page')
        articles = paginator.get_page(page)
        return render(request,"articles.html", {"articles":articles, "categories": categories})

    if keyword_date:
        article_list = Article.objects.filter(created_date__year = keyword_date)
        paginator = Paginator(article_list, NB_articles)
        page = request.GET.get('page')
        articles = paginator.get_page(page)
        return render(request,"articles.html", {"articles":articles, "categories": categories})

    article_list = Article.objects.all()
    paginator = Paginator(article_list, NB_articles)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    return render(request,"articles.html", {"articles":articles, "categories": categories})

def index(request):
    return redirect('articles/')

def about(request):
    return render(request,"about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {"articles":articles}

    return render(request,"dashboard.html", context)

@login_required(login_url = "user:login")
def addCategory(request):
    form = CategoryForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        category = form.save(commit=False)
        category.save()
        messages.success(request, "The category was successfully created")
        return redirect("article:dashboard")

    return render(request,"addarticle.html", {"form":form})

@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "The article was successfully created")
        return redirect("article:dashboard")

    return render(request,"addarticle.html", {"form":form})

def detail(request,id):
    article = get_object_or_404(Article, id = id)
    comments = article.comments.all()
    return render(request,"detail.html", {"article":article,"comments":comments})

@login_required(login_url = "user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Article was successfully updated")
        return redirect("article:dashboard")

    return render(request, "update.html", {"form":form})

@login_required(login_url = "user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)
    article.delete()
    messages.success(request, "Article was successfully deleted")

    return redirect("article:dashboard")

def addComment(request,id):
    article = get_object_or_404(Article,id = id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author  = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()

    return redirect(reverse("article:detail", kwargs={"id":id}))


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [config('EMAIL')])
            except BadHeaderError:
                messages.error(request, "Invalid Header Found")
                return redirect('../articles/')
            messages.success(request, "Email successfully sent")
            return redirect('../articles/')
    return render(request, "contact.html", {'form': form})

def handler404(request, exception, template_name='errors/404.html'):
    return render(request, 'errors/404.html', status=404)

def handler500(request, exception, template_name='errors/500.html'):
    return render(request, 'errors/500.html', status=500)
