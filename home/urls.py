
from django.urls import path
from . import views
from blog.views import blog_detail as bd
app_name='home'
urlpatterns = [
    path('', views.home, name='home'),
    path('verify-warranty/', views.verify_warrenty, name='verify_warrenty'),
    path('contact/', views.contact, name='contact'),
    path('contact-us/', views.contact_new, name='contact_new'),
    path('submit-stl-file/', views.stl, name='stl'),
    path('before-after/', views.beforeafter, name='beforeafter'),
    path('exhibition-gallery/', views.exhibition, name='exhibition'),
    path('career/', views.career, name='career'),
    path('event-gallery/<str:pk>/', views.eventgallery, name='eventgallery'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:pk>/', views.categoriesd, name='categoriesd'),
    path('blogs/', views.blogs, name='blogs'),
    path('search/', views.search, name='search'),
    path('gallery/', views.gallery, name='gallery'),
    path('terms-and-condition/', views.privacy, name='privacy'),
    path('cookie-policy/', views.cookie, name='cookie'),
    path('about-us/', views.about, name='about'),
    path('checkup/', views.checkup, name='checkup'),
    path('guest-posting/', views.gp, name='gp'),
    path('faq', views.faq, name='faq'),
    path('sitemap.xml/',views.sitemap, name='sitemap'),
    path('robots.txt/',views.robots, name='robot'),
    path('upload/', views.file_upload, name='upload'),
    path('testimonals/', views.testimonals, name='testimonals'),
    path('login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('services/', views.service_view, name='service_view'),
    
    path('client-profile/<str:pk>/<str:fk>/', views.ext_api, name='ext_api'),
    path('print-order/', views.print_order, name='print_order'),
    path('print-payment/', views.print_payment, name='print_payment'),
    path('print-statments/<str:pk>/<str:did>/', views.print_statment, name='print_statment'),
    path('print-invoice/<str:pk>/<str:did>/', views.print_invoice, name='print_invoice'),
    path('api-login/', views.api_user_login, name='api_user_login'),
    path('api-logout/<str:pk>/<str:did>/', views.api_logout, name='api_logout'),
    
    # path('Events/', views.ade_events, name='Events'),
    
    # path('best-dental-lab/', views.bdl, name='bdl'),
    path('best-dental-lab-in-<str:pk>/', views.bdld, name='bdld'),
    path('blog/<str:pk>/', bd, name='blogd'),
    path('quicks-links/', views.connect, name='connect'),
] 
    
