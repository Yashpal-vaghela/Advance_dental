from django.urls import path, include
from . import views
from blog.views import blog_detail as bd
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import *
from django.views.generic import RedirectView

app_name = 'home'
sitemaps_dict ={
    'home': HomePageSitemap,
    'static': StaticSitemap(),
    'normal': NormalPageSitemap,
    'blog': BlogSitemap,
    'product': ProductSitemap,  
    'webstory' : WebStorySitemap,
    'exhibition': ExhibitionSitemap,
    'bestDental': BestDentalLabSitemap
}

urlpatterns = [
    path('', views.home, name='home'),
    path('sitemap.xml', views.sitemap_index, name='sitemap-index'),
    path('sitemap-static.xml', views.static_sitemap, name='sitemap-static'),
    path('sitemap-products.xml', views.product_sitemap, name='sitemap-products'),
    path('sitemap-blog.xml', views.blog_sitemap, name='sitemap-blog'),
    path('sitemap-webstory.xml', views.webstory_sitemap, name='sitemap-webstory'),
    path('sitemap-exhibition.xml', views.exhibition_sitemap, name='sitemap-exhibition'),
    path('sitemap-bestDental.xml', views.bestdentallab_sitemap, name='sitemap-bestDental'),
    path('sitemap-news.xml', views.news_sitemap, name='sitemap-news'),
    path('contact/', views.contact, name='contact'),
    path('contact-us/', views.contact_new, name='contact_new'),
    path('submit-stl-file/', views.stl, name='stl'),
    path('before-after/', views.beforeafter, name='beforeafter'),
    path('exhibition-gallery/', views.exhibition, name='exhibition'),
    path('career/', views.career, name='career'),
    path('exhibition-gallery/<str:slug>/', views.eventgallery, name='eventgallery'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:pk>/', views.categoriesd, name='categoriesd'),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('search/', views.search, name='search'),
    path('gallery/', views.gallery, name='gallery'),
    path('terms-and-condition/', views.privacy, name='privacy'),
    path('cookie-policy/', views.cookie, name='cookie'),
    path('about-us/', views.about, name='about'),
    path('checkup/', views.checkup, name='checkup'),
    path('guest-posting/', views.gp, name='gp'),
    path('faq', views.faq, name='faq'),
    path('robots.txt/', views.robots, name='robot'),
    path('upload/', views.file_upload, name='upload'),
    path('testimonials/', views.testimonals, name='testimonals'),
    path('login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('web-story/', views.web_story, name='web_story'),
    path('web-story/<slug:story_slug>/', views.web_story_detail, name='web_story_detail'),
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
    path('best-dental-lab-in-<slug:slug>/', views.bdld, name='bdld'),
    path('blog/<str:slug>/', bd, name='blogd'),
    path('quicks-links/', views.connect, name='connect'),
    path('zirconia-crown/',views.zirconiacrown, name='zirconiacrown'),
    path('ad-implant/',views.adImplants, name='adImplants'),
    path('sitemap/',views.sitemap,name="sitemap"),
    path('404/',views.error_404,name="404"),
    path('verify-warrenty/', views.verify_warrenty, name='verify_warrenty'),
]
