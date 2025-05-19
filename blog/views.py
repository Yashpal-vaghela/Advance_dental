from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def blog_home(request):
    query = request.GET.get('q', '')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = []
        if query:
            matching_blogs = Blog.objects.filter(Q(title__icontains=query)).distinct()[:5]
            results = [{'title':blog.title,'id':blog.id,'slug':blog.slug} for blog in matching_blogs]
            return JsonResponse({'results':results})
        return JsonResponse({'results': []})
    
    all_blogs = Blog.objects.all().order_by('-published')
    remaining_blogs = all_blogs[2:]
    paginator=Paginator(remaining_blogs,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page = request.GET.get('page', 1)
    first_blog = page_obj.object_list[:2]
    all_blog = page_obj.object_list[2:]

    data2 =  Category.objects.all().order_by('-id')
    data3 = Blog.objects.filter(main3=True).order_by('-id')
    

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)


    context = {
        'first_blog':first_blog,
        'all_blog':all_blog,
        'data':data,
        'data2':data2,
        'data3':data3,
        'page_obj':page_obj
    }
    return render(request, 'blog_home.html', context)

# Create your views here.
def product_detail(request, slug):
    data = Product.objects.get(slug=slug)
    data2 =  SubProduct.objects.filter(product=data).order_by('-id')
    data3 = Blog.objects.filter(main3=True).order_by('-id')
    data4 = Faqpage.objects.filter(product=data).order_by('-id')
    
    context = {
        'data':data,
        'data2':data2,
        'data3':data3,
        'data4':data4,
    }
    return render(request, 'product_detail.html', context)


def blog_detail(request, slug):
    try:
        data = Blog.objects.get(slug=slug)
        blog_id = data.id
        data1 = Blog.objects.all().order_by('id')[:3]
        data2 =  Category.objects.all().order_by('-id')
        data3 = Blog.objects.filter(main3=True).order_by('-id')
        related_blogs = Blog.objects.filter(category__in=data.category.all()).exclude(id=data.id).distinct()

        context = {
            'data':data,
            'data1':data1,
            'data2':data2,
            'data3':data3,
            'related_blogs':related_blogs
        }
        return render(request, 'blog_detail.html', context)
    # except:
    #     pass

    except:
        data = Product.objects.get(slug= slug)
        data2 =  Category.objects.all().order_by('-id')
        data3 = Blog.objects.filter(main3=True).order_by('-id')
        data4 = Faqpage.objects.filter(product=data).order_by('-id')
        
        context = {
            'data':data,
            'data2':data2,
            'data3':data3,
            'data4':data4,
        }
        return render(request, 'product_detail.html', context)
    

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