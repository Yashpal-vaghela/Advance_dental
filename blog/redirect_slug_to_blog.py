import re
from django.http import HttpResponsePermanentRedirect
from blog.models import Blog, Product

class SlugToBlogRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.strip('/')

        # Skip if already under /blog/
        if not path.startswith('blog/'):
            try:
                # Check if a Blog with matching slug exists and is active
                blog_post = Blog.objects.get(slug=path, status=True)

                # Redirect to /blog/slug/
                return HttpResponsePermanentRedirect(f'/blog/{blog_post.slug}/')
            except Blog.DoesNotExist:
                pass  # No match, proceed normally

        return self.get_response(request)

class ProductToSlugRedirect:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        path = request.path.strip('/')

        if path.startswith('blog/'):
            slug = path[5:]
            try:
                product = Product.objects.get(slug=slug)
                return HttpResponsePermanentRedirect(f'/{product.slug}/')
            except Product.DoesNotExist:
                pass
        return self.get_response(request)        

class EventGalleryRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.strip('/')

        # Corrected the path prefix from 'even-gallery/' to 'event-gallery/'
        if path.startswith('event-gallery/'):
            slug = path[len('event-gallery/'):]
            return HttpResponsePermanentRedirect(f'/exhibition-gallery/{slug}/')

        return self.get_response(request)

class BestDentalLabRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.pattern = re.compile(r'^/best-dental-lab-in-[^/]+/')

    def __call__(self, request):
        path = request.path
        if self.pattern.match(path) and any(c.isupper() for c in path):
            return HttpResponsePermanentRedirect(path.lower())
        return self.get_response(request)