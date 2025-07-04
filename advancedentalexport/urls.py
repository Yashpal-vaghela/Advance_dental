from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blog.views import blog_detail as bd
from blog.views import product_detail as pd
from home import views as myapp_views
from django.conf.urls import handler404, handler500
from django.views.generic import RedirectView

# from exam import views as auth_view
admin.site.site_header = 'Dashboard'                    # default: "Django Administration"
admin.site.index_title = 'MIT Admin Panel'                 # default: "Site administration"
admin.site.site_title = 'My One Blog Admin Panel' # default: "Django site admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('sending-data/', include('enquiry.urls')),
    path('ultimate-smile-design/', include('usd.urls')),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),
    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # password reset
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='reset.html'), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='updatePW.html'), name="password_reset_confirm" ),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="complete.html"), name= "password_reset_complete"),
    path('blog/<str:slug>/', bd, name='blogd'),
    path('<str:slug>/', pd, name= 'productd' )
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

# handler404 = myapp_views.error_404
# handler500 = myapp_views.error_500