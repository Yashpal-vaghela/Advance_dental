from django.contrib.sitemaps import Sitemap
from django.utils.html import escape
from django.urls import reverse
from .models import Blog, Product, WebStory, Events, Place, Category, BeforeAfter, Gallery, EventsGallery

class HomePageSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return['home:home']
    def location(self, item):
        return reverse(item)
    
class BlogSitemap(Sitemap):
    def items(self):
        return ['blog-index'] + list(Category.objects.all()) + list(Blog.objects.filter(status=True).order_by('-updated'))

    def location(self, item):
        if item == 'blog-index':
            return '/blog/'
        elif isinstance(item, Category):
            return f"/blog/category/{item.slug}/"
        return item.get_absolute_url()

    def changefreq(self, item):
        return 'daily' if item == 'blog-index' else 'weekly'

    def priority(self, item):
        return 0.6

    def lastmod(self, item):
        return item.updated if isinstance(item, Blog) else None

    def image_urls(self, item):
        if isinstance(item, Blog) and item.image:
            return [{
                'loc': item.image.url,
                'title': item.title,
                'caption': item.description
            }]
        elif isinstance(item, Category) and item.image:
            return [{
                'loc': item.image.url,
                'title': item.meta_title,
                'caption': item.meta_description
            }]
        return []

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
                        'loc':'https://advancedentalexport.com/static/group-bg-img221.webp',
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
                'title': escape(obj.title),
                'description': escape(obj.description)
            }]
        return []

class WebStorySitemap(Sitemap):
    def items(self):
        return ['webstory-index'] + list(WebStory.objects.all().order_by('-publish_date'))

    def location(self, item):
        if item == 'webstory-index':
            return '/web-story/'
        return reverse('home:web_story_detail', kwargs={'story_slug': item.slug})

    def changefreq(self, item):
        return 'daily' if item == 'webstory-index' else 'weekly'

    def priority(self, item):
        return 0.6

    def lastmod(self, item):
        return None if item == 'webstory-index' else item.publish_date

    def image_urls(self, item):
        if item == 'webstory-index' or not item.image:
            return []
        return [{
            'loc': item.image.url,
            'title': item.title,
            'caption': item.description
        }]

    def video_urls(self, item):
        if item == 'webstory-index':
            return []
        return [{
            'thumbnail_loc': item.image.url,
            'title': item.title,
            'description': item.meta_description,
            'content_loc': video.video.url,
            'publication_date': str(item.publish_date)
        } for video in item.videos.all()]
    
class ExhibitionSitemap(Sitemap):

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
    
    def image_urls(self, item):
        image_list = []

        if item == 'before-after':
            before_after = BeforeAfter.objects.all()
            for obj in before_after:
                if obj.image:
                    image_list.append ({
                        'loc': obj.image.url,
                        'title': 'Before After - Advance Dental Export',
                        'caption': 'Explore Before & After Dental Solutions with Advance Dental Export. Elevate patient care with quality & innovation. Transform Your Practice!'
                    })
                
        elif item == 'gallery':
            gallery = Gallery.objects.all()
            for obj in gallery:
                if obj.image:
                    image_list.append({
                        'loc':obj.image.url,
                        'title': 'Gallery - Advance Dental Export',
                        'caption': "Explore Advance Dental Export's Gallery to see our innovative dental products and designs. Discover cutting-edge technology and creative exhibits today."
                    })
        elif isinstance(item, Events):
            event_images = EventsGallery.objects.filter(category=item)
            for img in event_images:
               if img.image: 
                    image_list.append({
                        'loc': item.image.url,
                        'title': f"ADE at {item.name}: Event Highlights and Gallery",
                        'caption': f"ADE at {item.name}: Event Highlights and Gallery"
                    })
        return image_list

class BestDentalLabSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Place.objects.all()
    
    def location(self, obj):
        return reverse('home:bdld', kwargs={'slug': obj.slug})
    
    def image_urls(self, obj):
        images = []
        if obj.image:
            images.append({
                'loc': obj.image.url,
                'title': escape(getattr(obj, 'meta_title','') or f"Best Dental Lab in {obj.name}"),
                'caption': escape(getattr(obj, 'meta_description', '') or f"Best Dental Lab in {obj.name}"),
            })
        return images
    
class NewsSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Blog.objects.filter(status=True).order_by('-updated')
    
    def location(self, obj):
        return obj.get_absolute_url()
    
    def image_urls(self, obj):
        images = []
        if obj.image:
            images.append({
                'loc': obj.image.url,
                'title': escape(obj.title or obj.h1),
                'caption': escape(obj.description)
            })
        return images
    
    def news_metadata(self, obj):
        return {
            'publication_name': "Advance Dental Export",
            'language': "en",
            'publication_date': obj.published.strftime("%Y-%m-%d"),
            'title': escape(obj.title or obj.h1),
        }