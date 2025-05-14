
from django.urls import path
from . import views
app_name='blog'
urlpatterns = [
    path('', views.blog_home, name='blog'),
    path('search-in-blogs', views.myblogsearch, name='myblogsearch'),
    path('all-blogs/', views.blog_list, name='blog_list'),
    path('all-blogs/<str:pk>/', views.cat_list, name='cat_list'),
    path('category-<slug:slug>/',views.category_view,name='category_view'),
    # path('blog_category/<str:pk>/',views.category_view,name='category_view')
    # path('search/', views.search_blogs, name='search_blogs'),
    # path('suggestions/', views.blog_suggestions, name='blog_suggestions'),
] 
