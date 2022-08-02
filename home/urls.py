from django.urls import path
from .views import *


urlpatterns = [
        path('', home , name ='home'),
        path('login/', Login, name='Login'),
        path('register/', register, name='register'),
        path('add-blog/', add_blog, name='add_blog'),
        path('see-blog/', see_blog, name='see_blog'),
        path('detail-blog/<slug>', detail_blog , name='detail_blog'),
        path('blog_update/<slug>/', blog_update, name='blog_update'),
        path('blog-delete/<id>', blog_delete, name='blog_delete'),
        path('logout/', logout_view, name='logout_view')
]
