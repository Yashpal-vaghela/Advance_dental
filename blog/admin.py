from django.contrib import admin
from .models import *

class BlogAdmin(admin.ModelAdmin):
    list_display=['h1']
    search_fields = ['title', 'h1', 'content','slug']
    class Media:
       js = ['ckeditor/ckeditor-init.js', 'ckeditor/ckeditor/ckeditor.js']

class WebStoryVideoInline(admin.TabularInline):
    model = WebStoryVideo
    extra = 5
    max_num = 10
    fields = ['video']  

class WebStoryAdmin(admin.ModelAdmin):
    inlines = [WebStoryVideoInline]
    list_display = ('title', 'publish_date', 'author')


# Register your models here.

admin.site.register(Blog, BlogAdmin)

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(ContactDetails)
admin.site.register(Tags)
admin.site.register(MostPopularBlog)
admin.site.register(Events)
admin.site.register(EventsGallery)
admin.site.register(NewEventLink)
admin.site.register(Product)
admin.site.register(SubProduct)
admin.site.register(Faqpage)
admin.site.register(Team)
admin.site.register(Testimonials)
admin.site.register(AboutImage)
admin.site.register(Client)
admin.site.register(Gallery)
admin.site.register(BeforeAfter)
admin.site.register(VideoTestimonals)
admin.site.register(Place)
admin.site.register(WebStory, WebStoryAdmin)
admin.site.register(WebStoryVideo)