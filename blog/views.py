from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q
from enquiry.forms import ContactForm
from django.contrib import messages
from django.conf import settings
import re
import requests
import threading
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from home.utils import send_mail

def send_email_async(context_dict):
    send_mail(
        to_email="vaghela9632@gmail.com",
        subject=f"New Contact Form Submission from {context_dict['Name']}",
        context_dict=context_dict,
    )


# Create your views here.
def blog_home(request):
    query = request.GET.get('q', '')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = []
        if query:
            try:
                tag = Tags.objects.get(tags__iexact=query)
            except Tags.DoesNotExist:
                tag = None

            matching_blogs = Blog.objects.filter(
                Q(title__icontains=query) | Q(tag__in=[tag])
            ).distinct()[:5]

            results = [{'title': blog.title, 'id': blog.id, 'slug': blog.slug} for blog in matching_blogs]
            return JsonResponse({'results': results})

        return JsonResponse({'results': []})

    # Get all blogs ordered by published date
    all_blogs = Blog.objects.all().order_by('-published')

    # Paginate all blogs in chunks of 8 (2 for first_blog, 6 for all_blog)
    paginator = Paginator(all_blogs, 8)
    page = request.GET.get('page', '1')

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    # Split the current page's blog into first and remaining
    first_blog = current_page.object_list[:2]
    all_blog = current_page.object_list[2:]

    # Other data
    data2 = Category.objects.all().order_by('-id')
    data3 = Blog.objects.filter(main3=True).order_by('-id')

    context = {
        'first_blog': first_blog,   
        'all_blog': all_blog,       
        'data': current_page,       
        'data2': data2,
        'data3': data3,
        'page_obj': current_page
    }

    return render(request, 'blog_home.html', context)

# Create your views here.
def product_detail(request, slug):
    data = Product.objects.get(slug=slug)
    data2 =  SubProduct.objects.filter(product=data).order_by('-id')
    data3 = Blog.objects.filter(main3=True).order_by('-id')
    data4 = Faqpage.objects.filter(product=data).order_by('-id')
    related_blogs = Blog.objects.filter(category__in=data.category.all()).distinct()
    author = Author.objects.first()
    print(related_blogs)
    context = {
        'data':data,
        'data2':data2,
        'data3':data3,
        'data4':data4,
        'related_blogs': related_blogs,
        'author': author,
    }
    return render(request, 'product_detail.html', context)

def inject_multiple_sections(html_content, inserts):
    # Remove tags → count words
    text_only = re.sub('<[^<]+?>', '', html_content)
    words = text_only.split()
    total_words = len(words)

    if total_words < 50:
        return html_content

    cutoffs = { int(total_words * pct): html for pct, html in inserts }

    current = 0
    result = ""
    pending_blocks = {}
    injected_blocks = set()
    inside_table = False

    tokens = re.split(r"(<[^>]+>)", html_content)

    closing_tags = [
        "</p>", "</ul>", "</ol>", "</li>", "</div>",
        "</section>", "</br>", "</h1>", "</h2>", "</h3>",
        "</h4>", "</table>"
    ]

    for token in tokens:

        # CASE 1 → HTML TAG
        if token.startswith("<"):

            # Detect entering table
            if token.lower().startswith("<table"):
                inside_table = True

            # Detect leaving table
            if token.lower().startswith("</table"):
                inside_table = False

            result += token

            # Try injection only if NOT inside table
            if not inside_table:
                for cutoff, html in list(pending_blocks.items()):
                    if cutoff not in injected_blocks:
                        if any(token.startswith(tag) for tag in closing_tags):
                            result += html
                            injected_blocks.add(cutoff)
                            pending_blocks.pop(cutoff, None)

        # CASE 2 → TEXT
        else:
            if token.strip():
                for w in token.split():
                    current += 1

                    # Mark pending cutoff
                    if current in cutoffs and current not in injected_blocks:
                        pending_blocks[current] = cutoffs[current]

                    result += w + " "
            else:
                result += token

    return result

def blog_detail(request, slug):
    # form = ContactForm(request.POST)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # recaptcha_response = request.POST.get("g-recaptcha-response")
        # data = {
        #     "secret": settings.RECAPTCHA_SECRET_KEY,
        #     "response": recaptcha_response,
        # }
        # r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        # result = r.json()

        # if not result.get('success'):
        #     messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        #     return redirect(request.META.get('HTTP_REFERER', 'contact'))
        if form.is_valid():
            submission = form.save()

            context_dict = {
                "Name": submission.name,
                "Email": submission.email,
                "Phone": submission.contact,
                "City": submission.city,
                "Subject": submission.subject,
                "Message": submission.message,
                "Page URL": request.META.get("HTTP_REFERER", "Not available"),
            }
            # send_mail(
            #     to_email="vaghela9632@gmail.com", 
            #     subject=f"New Contact Form Submission from {context_dict['Name']}",
            #     context_dict=context_dict,
            # )
            threading.Thread(
                target= send_email_async,
                args=(context_dict,),
                daemon=True
            ).start()

            bikai_payload  ={
               "Name": submission.name,
               "Email": submission.email,
               "Contact": submission.contact,
               "City": submission.city,
               "Subject": submission.subject,
               "Message": submission.message,
            }
            bikai_url = (
                "https://bikapi.bikayi.app/chatbot/webhook/YB4POk4LJXQxQk1pgmcYMCUMZwu1?flow=websitelea4344"
            )
            headers = {
                "Content-Type": "application/json",
            }
 
            try:
                crm_response = requests.post(
                    bikai_url,
                    json=bikai_payload,
                    headers=headers,
                    timeout=10,
                )
                crm_response.raise_for_status()
                messages.success(request, "Thanks for contacting the Advance Dental Export Team. We will get back to you shortly.")
            except requests.exceptions.RequestException as e:
                messages.warning(
                    request,
                    f"Form saved but could not send to CRM. Error: {str(e)}",
                )
            

            messages.success(
                request,
                "Thanks for contacting the Advance Dental Export Team. We will get back to you shortly."
            )
            return redirect(request.META.get('HTTP_REFERER', 'blog:blog'))
        else:
            messages.error(request, "Your form is not sent! Try again.")
            return redirect(request.META.get('HTTP_REFERER', 'blog:blog'))
    
        
    data = Blog.objects.get(slug=slug)
    blog_id = data.id
    data1 = Blog.objects.all().order_by('id')[:3]
    data2 =  Category.objects.all().order_by('-id')
    data3 = Blog.objects.filter(main3=True).order_by('-id')
    # related_blogs = Blog.objects.filter(category__in=data.category.all()).exclude(id=data.id).distinct()[1:4]
    gallery = Gallery.objects.all().order_by("-id")[:7]
    related_blogs = Blog.objects.all().order_by('-id')[1:4]
    product = Product.objects.all()
    priority_testimonials = Testimonials.objects.filter(priority=True).order_by('?')[:3]
    normal_testimonials = Testimonials.objects.filter(priority=False).order_by('?')[:6]
    products = [
                {id:1,"title":"AD-Implant","img":"explore-img1.webp","slug":"/ad-implant/"},
                {id:2,"title":"Advanced Aligners","img":"explore-img2.webp","slug":"/advanced-aligners/"},
                {id:3,"title":"Advance Zirconia","img":"explore-img3.webp","slug":"/zirconia-crown/"},
                {id:4,"title":"PFM Crown","img":"explore-img4.webp","slug":"/porcelain-fused-to-metal-pfm/"},
                {id:5,"title":"Aesthetic Maxima IPS Emax","img":"explore-img5.webp","slug":"/aesthetic-maxima/"},
            ]
    explore_50_html = render_to_string("custom-explore-product.html",{
        'product':products
    })
    # form_30_html = render_to_string("custom-search-form.html")
    section_70_html = render_to_string("custom-contact-form.html")

    data.content = mark_safe(
        inject_multiple_sections(
            data.content,
            inserts=[
                (0.30,explore_50_html),
                (0.70,section_70_html)
            ]
        )
    )

    context = {
        'data':data,
        'data1':data1,
        'data2':data2,
        'data3':data3,
        'related_blogs':related_blogs,
        'gallery':gallery,
        'priority_testimonials':priority_testimonials,
        'normal_testimonials':normal_testimonials,
        # 'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY,
    }

    return render(request,'blog_detail.html',context)

def myblogsearch(request):
    print('here')
    if request.method=="GET":
        q = request.GET.get('q')
    else:
        q= "a"    
    print(q)
    data1 = Blog.objects.filter(content__contains=q).order_by('-id')
    if data1:
        page = request.GET.get('page', 1)
        paginator = Paginator(data1, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

    else:
        data1 = Blog.objects.filter(content__contains="a").order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(data1, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
    data2 =  Category.objects.all().order_by('-id')
    data3 = Blog.objects.filter(main3=True).order_by('-id')
    context = {
        'data':data,
        'data2':data2,
        'data3':data3,
    }
    return render(request, 'blog_home.html', context)

def blog_list(request):
    data1 = Blog.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    
    paginator = Paginator(data1, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    response = render(request, 'blog_list.html', {'data' : data})
    try:
        page_num = int(page)
        if 2 <= page_num <= 10 :
            response['X-Robots-Tag'] = 'noindex, nofollow'
    except (ValueError, TypeError) :
        pass
    return response    

def cat_list(request, pk):
    
    data1 = Blog.objects.filter(category__id=pk).order_by('-id')
    page = request.GET.get('page', 1)

    
    paginator = Paginator(data1, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    context = {
        'data':data,
    }
    return render(request, 'blog_list.html', context)

def category_view(request, slug):
    # Remove 'category-' prefix if present in the slug
    # clean_slug = slug.replace('category-', '')

    try:
        # Get the category by slug (recommended to use a 'slug' field in Category model)
        final_category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return render(request, '404.html')  # Or handle gracefully

    # Filter blogs belonging to this category
    filtered_blogs = Blog.objects.filter(category=final_category).order_by('-id')

    # Optional: latest blogs for sidebar or other sections
    # all_blogs = Blog.objects.all().order_by('-id')
    paginator = Paginator(filtered_blogs,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page = request.GET.get('page',1)
    all_blogs = page_obj

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage: 
        data = paginator.page(paginator.num_pages)

    context = {
        'data': final_category,
        'blogs': filtered_blogs,
        'latest_blogs': all_blogs,
        'data1':data,
        'page_obj':page_obj,
        'all_blogs':all_blogs
    }
    return render(request, 'blog_category.html', context)   