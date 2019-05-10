from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Article
from django.core.paginator import Paginator
# Create your views here.


def hello_word(request):
    return HttpResponse('Hello,World!')


def article_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_content = article.brief_content
    content = article.content
    article_id = article.article_id
    publish_date = article.publish_date
    return_str = 'title: %s, brief_content: %s, content: %s, ' \
                 'article_id: %s, publish_date: %s' % (title, brief_content, content, article_id, publish_date)

    return HttpResponse(return_str)


def get_index_page(request):
    page = request.GET.get('page')
    print('page: ', page)
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)
    all_article = Article.objects.all()
    top5_article_list = Article.objects.order_by('-publish_date')[:5]
    paginator = Paginator(all_article, 3)
    page_num = paginator.num_pages
    print('page num: ', page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    return render(request, 'blog/index.html', {'article_list': page_article_list,
                                               'page_num': range(1,page_num + 1),
                                               'curr_page': page,
                                               'next_page': next_page,
                                               'previous': previous_page,
                                               'top5_article_list': top5_article_list})


def get_detail_page(request, article_id):
    all_articles = Article.objects.all()
    current_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None
    for index, article in enumerate(all_articles):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_articles) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        if article.article_id == article_id:
            current_article = article
            previous_article = all_articles[previous_index]
            next_article = all_articles[next_index]
            break

    return render(request, 'blog/detail.html', {'current_article': current_article,
                                                'previous_article': previous_article,
                                                'next_article': next_article})


def edit_article(request, article_id):
    if str(article_id) == '0':
        return render(request, 'blog/edit.html')
    article = Article.objects.get(pk=article_id)
    return render(request, 'blog/edit.html', {'article': article})


def edit_action(request):
    title = request.POST.get('title', 'TITLE')
    brief_content = request.POST.get('brief_content', 'BRIEF_CONTENT')
    content = request.POST.get('content', 'CONTENT')

    article_id = request.POST.get('article_id', '0')
    if article_id == '0':
        Article.objects.create(title=title, brief_content=brief_content, content=content)
        article = Article.objects.all()[0]
        return render(request, 'blog/detail.html', {'current_article': article,
                                                    'previous_article': article,
                                                    'next_article': article})

    article = Article.objects.get(pk=article_id)
    article.title = title
    article.brief_content = brief_content
    article.content = content
    article.save()
    article = Article.objects.get(pk=article_id)
    return render(request, 'blog/detail.html', {'current_article': article,
                                                'previous_article': article,
                                                'next_article': article})

