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
    def items(self):
        # Combine static identifier with Blog objects
        return ['blog-index'] + list(Blog.objects.filter(status=True).order_by('-updated'))

    def location(self, item):
        if item == 'blog-index':
            return '/blog/'
        return item.get_absolute_url()

    def changefreq(self, item):
        if item == 'blog-index':
            return 'daily'
        return 'weekly'

    def priority(self, item):
        if item == 'blog-index':
            return 0.6
        return 0.6  # or customize per item

    def lastmod(self, item):
        if item == 'blog-index':
            return None  # no <lastmod> tag for this
        return item.updated

class NormalPageSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['home:contact_new', 'home:beforeafter', 'home:gallery', 'home:testimonals', 'home:web_story', 'blog:blog']

    def location(self, item):
        return reverse(item)
    
class StaticSitemap(Sitemap):

    def items(self):
        return [
            {
                'name': 'home:home',
                'priority': 1.0,
                'changefreq': 'daily',
                'images': [{
                    'loc': 'https://advancedentalexport.com/static/img/feature.webp',
                    'title': 'Advance Dental Export | Certified Dental Labs in India',
                    'caption': 'Advance Dental Export is one of the best dental labs in India and a trusted dental prosthetics manufacturer, custom dental solutions for global clients since 2009.'
                }]
            },
            {
                'name': 'home:about',
                'priority':0.8,
                'changefreq':'weekly',
                'images': [
                    {
                        'loc':'https://advancedentalexport.com/static/img/team_about1.jpg',
                        'title':'About Us – Advance Dental Export',
                        'caption': 'Leader in Dental Implants, Cosmetic Dentistry &amp; Digital Dentistry. Providing top-notch Dental Lab Services for a perfect smile.'
                    },
                    {
                        'loc':'https://advancedentalexport.com/static/ade.jpeg',
                        'title':'About Us – Advance Dental Export',
                        'caption': 'Leader in Dental Implants, Cosmetic Dentistry &amp; Digital Dentistry. Providing top-notch Dental Lab Services for a perfect smile.'
                    }
                ]
            },
            {
                'name': 'home:contact_new',
                'priority': 0.6,
                'changefreq': 'weekly',
                'images': []
            },
            {
                'name': 'home:career',
                'priority': 0.6,
                'changefreq': 'weekly',
                'images': []
            },
            {
                'name': 'home:testimonals',
                'priority': 0.6,
                'changefreq': 'weekly',
                'images': []
            },
            {
                'name': 'home:sitemap',
                'priority': 0.6,
                'changefreq':'weekly',
                'images':[]
            }
            ]
    
    def location(self, item):
        return reverse(item['name'])

    def changefreq(self, item):
        return item.get('changefreq', 'monthly')

    def priority(self, item):
        return item.get('priority', 0.5)

    def image_urls(self, item):
        return [
            {
                'loc': img['loc'],
                'title': img.get('title'),
                'caption': img.get('caption'),
            }
            for img in item.get('images', [])
        ]
    
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all().order_by('-updated')

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
    def items(self):
        # Combine static path with dynamic objects
        return ['webstory-index'] + list(WebStory.objects.all().order_by('-publish_date'))

    def location(self, item):
        if item == 'webstory-index':
            return '/web-story/'
        return reverse('home:web_story_detail', kwargs={'story_slug': item.slug})

    def changefreq(self, item):
        if item == 'webstory-index':
            return 'daily'
        return 'weekly'

    def priority(self, item):
        return 0.6

    def lastmod(self, item):
        if item == 'webstory-index':
            return None
        return item.publish_date
    
class ExhibitionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        # static + dynamic
        return ['exhibition-index', 'before-after', 'gallery'] + list(Events.objects.all())

    def location(self, item):
        if item == 'exhibition-index':
            return '/exhibition-gallery/'
        elif item == 'before-after':
            return '/before-after/'
        elif item == 'gallery':
            return '/gallery/'
        return reverse('home:eventgallery', kwargs={'slug': item.slug})

    def changefreq(self, item):
        return 'weekly'

    def priority(self, item):
        return 0.6

    def lastmod(self, item):
        return None   

class BestDentalLabSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Place.objects.all()
    
    def location(self, obj):
        return reverse('home:bdld', kwargs={'slug': obj.slug})
