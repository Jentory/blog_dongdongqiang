from django.urls import path,include

import blog.views

urlpatterns = [
    path('hello_word', blog.views.hello_word),
    path('content', blog.views.article_content),
    path('index', blog.views.get_index_page),
    # path('detail', blog.views.get_detail_page),
    path('detail/<int:article_id>', blog.views.get_detail_page)
]

