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
            matching_blogs = Blog.objects.filter(Q(title__icontains=query) | Q(tags__icontains=query))[:5]
            results = [{'title':blog.title,'id':blog.id,'slug':blog.slug} for blog in matching_blogs]
            return JsonResponse({'results':results})
        
    data1 = Blog.objects.all().order_by('-id')
    data2 =  Category.objects.all().order_by('-id')
    data3 = Blog.objects.filter(main3=True).order_by('-id')
    
    paginator = Paginator(data1, 12)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    page = request.GET.get('page', 1)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)


    context = {
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
        context = {
        'data':data,
        'data1':data1,
        'data2':data2,
        'data3':data3,
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

def category_view(request,slug):
    # category = get_object_or_404(Category,slug=pk)
    # SingleCatgory = Category.objects.get(slug=pk)
    # posts = Category.objects.all().order_by('-id')
    # blogcategory = Blog_Category.objects.all()
    # print("blog_category",blogcategory)
    # print("slug",pk,"SingleCatgory",category_id,"finalCategoryData",finalCategoryData,"filter",final1)
    clean_slug = slug.replace('category-','').replace('category-','').capitalize()
    # category = get_object_or_404(Category,slug=clean_slug)
    # product = Category.objects.filter(category=category)

    finalCategoryData = Category.objects.get(category=clean_slug)
    category_id = finalCategoryData.id
    filterBlogData = Blog.objects.filter(category=category_id)
    filterBlogData1 = Blog.objects.all().order_by('-id')
    # final1 = Category.objects.filter(id=category_id)
    print('clean',slug,'product',clean_slug,"final","sds",category_id)
    # print("filterBlogData",filterBlogData,"finalCatgeoryData",finalCategoryData,"clean",clean_slug)

    context = {
        'category':filterBlogData,
        'data':filterBlogData1
    }
    return render(request,'blog_category.html',context)