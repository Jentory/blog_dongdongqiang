from django.urls import path,include

import blog.views

app_name = 'blog'

urlpatterns = [
    path('hello_word', blog.views.hello_word, name='helloword'),
    path('content', blog.views.article_content, name='content'),
    path('index', blog.views.get_index_page, name='index'),
    # path('detail', blog.views.get_detail_page),
    path('detail/<int:article_id>', blog.views.get_detail_page, name='detail'),
    path('edit/<int:article_id>', blog.views.edit_article, name='edit'),
    path('editaction', blog.views.edit_action, name='editaction')
]

