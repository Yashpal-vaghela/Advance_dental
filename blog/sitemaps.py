from django.contrib.sitemaps import Sitemap
from django.utils.html import escape
from django.urls import reverse
from .models import Blog, Product, WebStory, Events, Place

class HomePageSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return['home:home']
    def location(self, item):
        return reverse(item)
    
class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Blog.objects.filter(status=True).order_by('-updated')

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()

class NormalPageSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['home:contact_new', 'home:beforeafter', 'home:gallery', 'home:testimonals', 'home:web_story', 'blog:blog']

    def location(self, item):
        return reverse(item)
    
class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home:about']
    
    def location(self, item):
        return reverse(item)
    
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(status=True).order_by('-updated')

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()

    def image_urls(self, obj):
        if obj.image:
            return [{
                'loc': obj.image.url,
                'title': escape(obj.title)
            }]
        return []
class WebStorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return WebStory.objects.all().order_by('-publish_date')

    def lastmod(self, obj):
        return obj.publish_date

    def location(self, obj):
        return reverse('home:web_story_detail', kwargs={'story_slug': obj.slug})
    
class ExhibitionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Events.objects.all()

    def location(self, obj):
        return reverse('home:eventgallery', kwargs={'slug': obj.slug})    

class BestDentalLabSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Place.objects.all()
    
    def location(self, obj):
        return reverse('home:bdld', kwargs={'pk': obj.name})
