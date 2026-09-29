import re
from django.http import HttpResponsePermanentRedirect
from blog.models import Blog, Product, RedirectRule

class DynamicRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Exclude admin panel, static assets, and media files from dynamic redirection
        if path.startswith(('/admin/', '/static/', '/media/')):
            return self.get_response(request)

        full_path = request.get_full_path()
        stripped_path = path.strip('/')

        possible_old_urls = [
            full_path,
            path,
            stripped_path,
            f"/{stripped_path}",
            f"/{stripped_path}/",
            f"{stripped_path}/"
        ]

        try:
            active_redirects = RedirectRule.objects.filter(
                is_active=True,
                old_url__in=possible_old_urls
            )
            if active_redirects.exists():
                redirect_map = {r.old_url: r for r in active_redirects}
                redirect_obj = None
                for candidate in possible_old_urls:
                    if candidate in redirect_map:
                        redirect_obj = redirect_map[candidate]
                        break

                if redirect_obj:
                    target_url = redirect_obj.new_url.strip()
                    if not (target_url.startswith('http://') or target_url.startswith('https://') or target_url.startswith('/')):
                        target_url = '/' + target_url

                    # Avoid infinite redirect loop
                    if target_url != full_path and target_url != path and target_url != stripped_path and target_url != f"/{stripped_path}/":
                        return HttpResponsePermanentRedirect(target_url)
        except Exception:
            pass

        return self.get_response(request)

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