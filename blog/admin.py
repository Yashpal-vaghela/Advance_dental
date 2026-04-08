from django.contrib import admin
from .models import *
from django.utils.html import strip_tags

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

class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')
    search_fields = ['name']

class TeamAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'name')
    list_editable = ('display_order',)
    list_display_links = ("name",) 
    ordering = ('display_order',)

@admin.register(ImageSearch)
class ImageUsageSearchAdmin(admin.ModelAdmin):
    change_list_template = "admin/image_usage_search.html"
    list_display = ()
    search_fields = ()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return ImageSearch.objects.none()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        query = request.GET.get("q", "").strip()
        usage_results = []

        def build_change_url(obj):
            return reverse(
                f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
                args=[obj.pk]
            )

        def add_image_result(obj, model_name, field_name, file_field, label_attr=None):
            if not file_field:
                return

            file_name = getattr(file_field, "name", "")
            if not file_name:
                return

            short_name = file_name.split("/")[-1]

            if query.lower() in file_name.lower() or query.lower() in short_name.lower():
                title = getattr(obj, label_attr) if label_attr and hasattr(obj, label_attr) else str(obj)
                alt_value = getattr(obj, "alt", None)
                usage_results.append({
                    "model": model_name,
                    "title": title,
                    "field": field_name,
                    "alt": alt_value if alt_value else "❌ Missing ALT",
                    "matched_value": file_name,
                    "url": build_change_url(obj),
                })

        def add_text_result(obj, model_name, field_name, text_value, label_attr=None):
            if not text_value:
                return

            text_value = str(text_value)
            if query.lower() in text_value.lower():
                title = getattr(obj, label_attr) if label_attr and hasattr(obj, label_attr) else str(obj)

                plain_text = strip_tags(text_value)
                plain_text = " ".join(plain_text.split())

                index = plain_text.lower().find(query.lower())
                if index != -1:
                    start = max(index - 60, 0)
                    end = min(index + len(query) + 120, len(plain_text))
                    snippet = plain_text[start:end]
                else:
                    snippet = plain_text[:180]

                usage_results.append({
                    "model": model_name,
                    "title": title,
                    "field": field_name,
                    "match_type": "Content/HTML",
                    "matched_value": snippet,
                    "url": build_change_url(obj),
                })

        if query:
            # Category
            for obj in Category.objects.filter(image__icontains=query):
                add_image_result(obj, "Category", "image", obj.image, "category")

            # Author
            for obj in Author.objects.filter(image__icontains=query):
                add_image_result(obj, "Author", "image", obj.image, "name")

            # Blog
            for obj in Blog.objects.filter(image__icontains=query):
                add_image_result(obj, "Blog", "image", obj.image, "h1")
            for obj in Blog.objects.filter(content__icontains=query):
                add_text_result(obj, "Blog", "content", obj.content, "h1")
            for obj in Blog.objects.filter(edits__icontains=query):
                add_text_result(obj, "Blog", "edits", obj.edits, "h1")

            # Product
            for obj in Product.objects.filter(image__icontains=query):
                add_image_result(obj, "Product", "image", obj.image, "h1")
            for obj in Product.objects.filter(content__icontains=query):
                add_text_result(obj, "Product", "content", obj.content, "h1")
            for obj in Product.objects.filter(edits__icontains=query):
                add_text_result(obj, "Product", "edits", obj.edits, "h1")

            # SubProduct
            for obj in SubProduct.objects.filter(image__icontains=query):
                add_image_result(obj, "SubProduct", "image", obj.image, "h1")
            for obj in SubProduct.objects.filter(blog_banner_lg__icontains=query):
                add_image_result(obj, "SubProduct", "blog_banner_lg", obj.blog_banner_lg, "h1")
            for obj in SubProduct.objects.filter(blog_banner_sm__icontains=query):
                add_image_result(obj, "SubProduct", "blog_banner_sm", obj.blog_banner_sm, "h1")
            for obj in SubProduct.objects.filter(content__icontains=query):
                add_text_result(obj, "SubProduct", "content", obj.content, "h1")
            for obj in SubProduct.objects.filter(edits__icontains=query):
                add_text_result(obj, "SubProduct", "edits", obj.edits, "h1")

            # AboutPage
            for obj in AboutPage.objects.filter(image__icontains=query):
                add_image_result(obj, "AboutPage", "image", obj.image, "title")
            for obj in AboutPage.objects.filter(why_choose_us_img__icontains=query):
                add_image_result(obj, "AboutPage", "why_choose_us_img", obj.why_choose_us_img, "title")
            for obj in AboutPage.objects.filter(why_choose_us_img_1__icontains=query):
                add_image_result(obj, "AboutPage", "why_choose_us_img_1", obj.why_choose_us_img_1, "title")

            # Team
            for obj in Team.objects.filter(image__icontains=query):
                add_image_result(obj, "Team", "image", obj.image, "name")

            # Testimonials
            for obj in Testimonials.objects.filter(image__icontains=query):
                add_image_result(obj, "Testimonials", "image", obj.image, "name")

            # Events
            for obj in Events.objects.filter(image__icontains=query):
                add_image_result(obj, "Events", "image", obj.image, "name")

            # EventsGallery
            for obj in EventsGallery.objects.filter(image__icontains=query):
                add_image_result(obj, "EventsGallery", "image", obj.image, "name")

            # NewEventLink
            for obj in NewEventLink.objects.filter(cover_image__icontains=query):
                add_image_result(obj, "NewEventLink", "cover_image", obj.cover_image, "name")
            for obj in NewEventLink.objects.filter(skyline_image__icontains=query):
                add_image_result(obj, "NewEventLink", "skyline_image", obj.skyline_image, "name")

            # AboutImage
            for obj in AboutImage.objects.filter(image__icontains=query):
                add_image_result(obj, "AboutImage", "image", obj.image, "name")

            # Client
            for obj in Client.objects.filter(image__icontains=query):
                add_image_result(obj, "Client", "image", obj.image, "name")

            # Gallery
            for obj in Gallery.objects.filter(image__icontains=query):
                add_image_result(obj, "Gallery", "image", obj.image, "name")

            # BeforeAfter
            for obj in BeforeAfter.objects.filter(image__icontains=query):
                add_image_result(obj, "BeforeAfter", "image", obj.image, "name")

            # Place
            for obj in Place.objects.filter(image__icontains=query):
                add_image_result(obj, "Place", "image", obj.image, "name")

            # WebStory
            for obj in WebStory.objects.filter(image__icontains=query):
                add_image_result(obj, "WebStory", "image", obj.image, "title")

        extra_context["usage_results"] = usage_results
        extra_context["query"] = query
        extra_context["title"] = "Image Usage Search"
        return super().changelist_view(request, extra_context=extra_context)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

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
admin.site.register(Team, TeamAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(AboutImage)
admin.site.register(Client)
admin.site.register(Gallery)
admin.site.register(BeforeAfter)
admin.site.register(VideoTestimonals)
admin.site.register(Place)
admin.site.register(WebStory, WebStoryAdmin)
admin.site.register(WebStoryVideo)
admin.site.register(Award, AwardAdmin)