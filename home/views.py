import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse, FileResponse, Http404, HttpResponse
from blog.models import *
from enquiry.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from enquiry.forms import STLForm, STLFileForm, LoginForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import requests
from blog.sitemaps import *
from enquiry.forms import ContactForm, CareerForm, CareerFileForm

# from enquiry.models import InstaPost
# Create your views here.
def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        # reCAPTCHA validation
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        if not result.get("success"):
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
            return redirect(request.META.get("HTTP_REFERER", "home:home"))

        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect("home:home")
        else:
            messages.error(request, "Your query was not sent! Try again.")
            return redirect(request.META.get("HTTP_REFERER", "home:home"))
    else:
        form = ContactForm()

    # Non-POST: load homepage data
    main3 = Blog.objects.filter(main3=True).order_by("-id")[:3]
    data = Testimonials.objects.all().order_by("-id")[:20]
    data2 = Blog.objects.all().order_by("-id")[:3]
    client = Client.objects.all().order_by("-id")
    gallery = Gallery.objects.all().order_by("-id")[:7]
    gallery21 = BeforeAfter.objects.all().order_by("-id")[:7]
    video = VideoTestimonals.objects.all().order_by("-id")[:4]

    context = {
        "main3": main3,
        "data": data,
        "data2": data2,
        "client": client,
        "gallery": gallery,
        "gallery21": gallery21,
        "video": video,
        "form": form,
        "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
    }
    return render(request, "index.html", context)

def testimonals(request):
    videoData = VideoTestimonals.objects.all()
    data = Testimonials.objects.all().order_by('-id')[:20]
    context = { 
        'videoData':videoData,
        'data':data,
    }
    return render(request, 'testimonals.html', context)


def verify_warrenty(request):
    
    # Input parameters
    
    
    if request.method == 'POST':
        orderId = request.POST.get('id') 
        authenticationId = request.POST.get('auth') 
        # Set your parameters
        api_url = "https://adesurat.com/API.php?call=get_warranty_details"
        orderId = str(orderId)
        authenticationId = str(authenticationId)
        
        # Data to be sent in form-encoded format
        data = {
            "authenticationId": authenticationId,
            "orderId": orderId
        }
        
        # Make the POST request with data as form-encoded
        response = requests.post(api_url, data=data)
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            # Extract data from the "data" object
            warranty_data = data.get("data", {})
            status = data.get("status", False)
            # Pass data to template
            
            return render(request, 'verify_warrenty_r.html', {'status': status, 'warranty_data': warranty_data})
        else:
            # If request fails, handle it appropriately
            messages.error(request, 'Your Warrenty Card Is Invalid')
            return redirect('home:verify_warrenty')
        
    return render(request, 'verify_warrenty.html')


def blogd(request, pk):
    data =  Blog.objects.get(slug=pk)
    data2 =  Blog.objects.all().order_by('-id')[:2]
    cat = None
    for ie in data.category.all():
        cat = ie.category
        print(cat)
    data3 =  Category.objects.get(category=cat) if cat else None
    context = {
        'data':data,
        'data2':data2,
        'data3':data3,
    
    }
    return render(request, 'blogd.html', context)


# def contact(request):
#     if request.method == "POST":
#         form = ContactForm(request.POST)

#         recaptcha_response = request.POST.get("g-recaptcha-response")
#         data ={
#             "secret": settings.RECAPTCHA_SECRET_KEY,
#             "response": recaptcha_response,
#         }
#         verify_url = "https://www.google.com/recaptcha/api/siteverify"
#         r = requests.post(verify_url, data=data)
#         result = r.json()

#         if result.get("success"):
#             ContactDetails.objects.create(
#                 name=request.POST.get("name"),
#                 email=request.POST.get("email"),
#                 contact=request.POST.get("contact"),
#                 subject=request.POST.get("subject"),
#                 message=request.POST.get("message"),
#             )
#             messages.success(request, "Your message has been sent successfully.")
#             return redirect("contact")
#         else:
#             messages.error(request,"Invalid reCAPTCHA. Please try again")
#     data= ContactDetails.objects.all()
#     context = {
#         'data':data,
#         'recaptcha_site_key' : settings.RECAPTCHA_SITE_KEY,
#     }
#     return render(request, 'contact.html', context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        recaptcha_response = request.POST.get("g-recaptcha-response")
        data ={
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect(request.META.get('HTTP_REFERER','contact'))
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your data is sent successfully.')
            return redirect('home: contact')
        else:
            messages.error(request, 'Your query is not sent! Try Again.')
            return redirect(request.META.get('HTTP_REFERER', 'contact'))

    context = {
        "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY
    }
    return render(request, 'contact.html', context)

def contact_new(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        recaptcha_response = request.POST.get("g-recaptcha-response")
        data ={
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect(request.META.get('HTTP_REFERER','contact'))
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your data is sent successfully.')
            return redirect('home:contact_new')
        else:
            messages.error(request, 'Your query is not sent! Try Again.')
            return redirect(request.META.get('HTTP_REFERER', 'contact'))
    else:
        form = ContactForm()
    return render(
        request,
        "contact_new.html",
        {"form": form, "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY},
    )

        
def connect(request):
    context = {
        'hide_social_image': True,
    }
    return render(request, 'connect.html', context)
    
def career(request):
    if request.method == 'POST':
        career_form = CareerForm(request.POST)
        resume_file = request.FILES.get('files')

        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            'secret' : settings.RECAPTCHA_SECRET_KEY,
            'response' : recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        if career_form.is_valid() and resume_file:
            # Create career object
            career_obj = career_form.save(commit=False)
            career_obj.save()

            # if not result.get("success"):
            #     messages.error(request, "Invalid reCAPTCHA. Please try again.")
            #     return redirect(request.META.get("HTTP_REFERER", "home:career"))

            # Attach file
            career_file_form = CareerFileForm(
                {'career': career_obj.id},
                {'resume': resume_file}
            )

            if career_file_form.is_valid():
                career_file_form.save()
                messages.success(request, 'Your career application has been submitted successfully.')
                return redirect('home:career')
            else:
                # rollback career_obj if file form fails
                career_obj.delete()
                for field, errors in career_file_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")

        else:
            # Collect errors for missing resume or invalid career_form
            if not resume_file:
                messages.error(request, "Please upload your resume before submitting.")

            if not career_form.is_valid():
                for field, errors in career_form.errors.items():
                    for error in errors:
                        if field == "__all__":
                            messages.error(request, error)
                        else:
                            messages.error(request, f"{field.capitalize()}: {error}")

    else:
        career_form = CareerForm()

    context = {
        'career_form': career_form,
        "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
    }
    return render(request, 'career.html', context)



def exhibition(request):
    context = {
    }
    return render(request, 'exhibition.html', context)

def zirconiacrown(request):
    cards = [
        {"title": "Planning","subtitle": "Plan The Treatment","image": "img/try1.webp", "alt":"Zirconia dental treatment planning for customized and precise restorative care solutions"},
        {"title": "Presentation", "subtitle": "Present The Treatment", "image": "img/try2.webp", "alt":"Zirconia dental treatment plan presentation to patient for personalized restorative care"},
        {"title": "Accuracy", "subtitle": "Provide Accurate And Reliable Results","image": "img/try3.webp", "alt":"Digital display showing zirconia dental treatment plan for advanced restorative procedures" },
        {"title": "Preparation","subtitle": "Custom Restoration Preparation","image": "img/try4.webp", "alt":"Custom zirconia dental restoration preparation for precise and personalized patient treatment"},
        {"title": "Provision","subtitle": "Provide The Temporaries","image": "img/try5.webp", "alt":"Placement phase of zirconia dental treatment temporaries for trial fit and aesthetic evaluation"},
        {"title": "Collection","subtitle": "Collect Smile Data","image": "img/try6.webp", "alt": "Completed zirconia dental treatment with successful results at Advance Dental Export laboratory"},
    ]
 
    Benefit = [
        {
            'id':'01',
            'title':"Protects Opposing Teeth",
            'imgUrl':"011Benefit.svg",
            'description':"Gentle yet strong, Advance Zirconia helps reduce wear on the teeth it bites against. It protects your natural teeth while still offering long-lasting durability.", 
            'alt':"Advance Zirconia SVG icon showing strong yet gentle protection for opposing natural teeth"
        },
        {
            'id':'02','title':"Longevity",
            'imgUrl':"02Benefit.svg",
            'description':"Designed for long-term use, Advance Zirconia resists chipping, cracking, and decay, offering a reliable and durable solution that stands the test of time.", 
            'alt':"Icon depicting Advance Zirconia’s durability resisting chips, cracks, and decay for long-lasting use"
        },
        {
            'id':'03',
            'title':"Precision and Fit",
            'imgUrl':"03Benefit.svg",
            'description':"Crafted using advanced technology, Advance Zirconia crowns provide a custom fit that ensures comfort, stability, and a natural bite alignment.", 
            'alt':"Icon representing precise custom fit and advanced technology of Advance Zirconia crowns for comfort"
        },
        {
            'id':'04',
            'title':"Versatility",
            'imgUrl':"04Benefit.svg",
            'description':"Advance Zirconia is suitable for a wide range of dental treatments—including crowns, bridges, and implants—delivering dependable performance with a natural look.", 
            'alt':"Icon illustrating Advance Zirconia’s versatility for crowns, bridges, and implants with natural aesthetics"
        },
        {
            'id':'05',
            'title':"Aesthetics",
            'imgUrl':"05Benefit.svg",
            'description':"With its lifelike translucency and excellent color-matching, Advance Zirconia creates a seamless, beautiful restoration that blends perfectly with your natural teeth.", 
            'alt':"Advance Zirconia icon for lifelike translucency and color-matching in natural-looking restorations"
        },
        {
            'id':'06',
            'title':"Metal-Free Material",
            'imgUrl':"06Benefit.svg",
            'description':"Made without any metal, Advance Zirconia is a great option for people who are allergic or sensitive to metals. It’s safe, comfortable, and looks more natural, too.", 
            'alt':"Metal-free Advance Zirconia icon showing safe, natural option for metal-sensitive dental patients"
        },
        {
            'id':'07',
            'title':"Minimal Tooth Removal",
            'imgUrl':"07Benefit.svg",
            'description':"Advance Zirconia allows for thinner, stronger restorations. Your dentist can remove less enamel, helping preserve more of your natural tooth structure.", 
            'alt':"Advance Zirconia icon representing minimal tooth removal and preservation of natural enamel structure"
        },
        {
            'id':'08',
            'title':"Resistance To Staining",
            'imgUrl':"08Benefit.svg",
            'description':"Thanks to its smooth, non-porous finish, Advance Zirconia resists stains from coffee, tea, or wine, keeping your smile bright and clean over time.", 
            'alt':"Advance Zirconia icon showing stain resistance from coffee, tea, and wine for a lasting bright smile"
        },
        {
            'id':'09',
            'title':"Gum-Friendly Surface",
            'imgUrl':"09Benefit.svg",
            'description':"Its smooth surface helps prevent plaque from building up around the crown, making it easier to keep your gums clean and healthy.", 
            'alt':"Advance Zirconia icon showing smooth, gum-friendly surface that resists plaque buildup for oral health"
        },
    ]

    faq_data =[
        {
            "question": "What is zirconia in dentistry?",
            "answer": "Zirconia, or zirconium dioxide, is a durable ceramic material used in dental restorations like crowns and bridges. It's known for its strength, biocompatibility, and natural tooth-like appearance, making it a popular choice for both front and back teeth restorations."
        },
        {
            "question": "How much do zirconia crowns or teeth cost?",
            "answer": "In India, the cost of a zirconia crown can vary based on factors like the complexity of the case, the specific type of zirconia used, and the dental laboratory's expertise. Concult us for detailed pricing & treatment details tailored to your needs."
        },
        {
            "question": "Is zirconia a good material for dental restorations?",
            "answer": "Yes, zirconia is highly regarded for dental restorations due to its exceptional strength, resistance to wear, and compatibility with the human body. It also offers excellent aesthetics, closely resembling natural teeth, which makes it suitable for various dental applications."
        },
        {
            "question": "How long do zirconia crowns usually last?",
            "answer": "Zirconia crowns are known for their longevity, often lasting between 10 to 15 years or more with proper oral hygiene and regular dental check-ups. Some reports even suggest they can last up to 20 years or longer."
        },
        {
            "question": "Why do dentists use zirconia for dental restorations?",
            "answer": "Dentists prefer zirconia for its superior strength, durability, and natural appearance. It's also biocompatible, reducing the risk of allergic reactions, and can be precisely crafted using digital technology, ensuring a better fit and comfort for patients."
        }
    ]

    return render(request, 'zir.html',  {'cards': cards,'Benefit':Benefit, 'faq_data': faq_data})

# def neweventlink(request):
#     context = {
#     }
#     return render(request, 'exhibition.html', context)

def adImplants(request):
    faq_data = [
    {
        "question": "What is a dental implant for teeth, and how does it work?",
        "answer": "A dental implant for tooth is a small, screw-like post made of titanium or zirconia that replaces the root of a missing tooth. It's surgically placed into the jawbone, where it fuses with the bone over time. Once integrated, a crown is attached to restore the appearance and function of a natural tooth."
    },
    {
        "question": "What are the different types of dental implants?",
        "answer": "The main three types of implants include: Endosteal Implants, Subperiosteal Implants, and Zygomatic Implants."
    },
    {
        "question": "Are dental implants safe and reliable?",
        "answer": "Yes, dental implants for teeth are considered safe and have a high success rate. They are made from biocompatible materials like titanium, which are well-tolerated by the body. With proper care and oral hygiene, implants can provide a durable and long-lasting solution for missing teeth."
    },
    {
        "question": "How much do dental implants cost in India?",
        "answer": "The cost of dental implants in India varies based on factors like the type of Implant, number of Implants needed, and materials used. For an accurate estimate tailored to your specific needs, consult with us to provide a detailed treatment plan & cost."
    },
    {
        "question": "How long do dental teeth implants usually last?",
        "answer": "Dental implants are designed to be a long-term solution and can last 10 to 20 years or more with proper care. Factors influencing their longevity include oral hygiene practices, regular dental check-ups, and overall health."
    }
]
    context={
        'faq_data' : faq_data
    }
    return render(request,'ad-Implant.html', context)


def beforeafter(request):
    data = BeforeAfter.objects.all()
    context = {
        'data':data,
    }
    return render(request, 'beforeafter.html', context)

def stl(request):
            
    if request.method == 'POST':
        
        documents = request.FILES.getlist('files')
        
        nam = request.POST.get('name')
        phone = request.POST.get('contact')
        message = request.POST.get('message')
        name = STLFile.objects.create(name=nam, contact=phone, message=message)

        name.save()
        name = STLFile.objects.all().last()
        
        for f in documents:
            pp = STLFileData.objects.create(stl_data=name, files=f)
            pp.save()

        html_content = render_to_string ('stlmail.html',{ 
            'name':nam, 'phone':phone, 'message':message
        })
        email_from = settings.EMAIL_HOST_USER
        subject = 'New Data In STL Form'
        message = "You have a new data in STL form."
        recipient_list = ['stl@advancedentalexport.com']
        # send_mail( subject, message, email_from, recipient_list, html_message=html_content, fail_silently=False )

        messages.success(request, 'Your STL File Is Uploaded Successfully')
        # return redirect('home:home')  
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  




    d = STLFileForm()
    context = {
    'd':d
    }
    return render(request, 'stl.html', context)



def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.getlist('files')
        print(my_file)
        for f in my_file:
            print('a')

        return HttpResponse('')
    return JsonResponse({'post':'fasle'})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home:dashboard')
    else:
        if request.method == "POST":
            # your sign in logic goes here
            form = LoginForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                #authenticate checks if credentials exists in db
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('home:dashboard')

                    else:
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

                        
                else:
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    context = {
    
    }
    return render(request, 'login.html', context)
    


@login_required(login_url = 'home:user_login')
def dashboard(request):
    if request.user.is_staff:
        data = STLFile.objects.all().order_by('-id')
        context = {
            'data':data,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('home:home')

def singUser(request):
    context = {
    }
    return render(request, 'singup.html', context)


def eventgallery(request, slug):
    
    data1 =  EventsGallery.objects.filter(category__slug=slug).order_by('-id')
    cat = Events.objects.get(slug=slug)
    page = request.GET.get('page', 1)
    paginator = Paginator(data1, 12)
    meta_description = cat.meta_description
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    response = render(request, 'eventgallery.html', {'data': data, 'cat': cat, 'slug': slug, 'meta_description': meta_description })
    # Add noindex for specific pages (e.g., ?page=2 and onward)
    try:
        page_num = int(page)  # Convert page to integer
        if page_num >= 3:  # Apply noindex to pages 2 and beyond
            response['X-Robots-Tag'] = 'noindex, nofollow'
    except (ValueError, TypeError):
        pass  # Ignore if the page is not a valid number

    return response



def about(request):
    team = Team.objects.all()
    imagez = AboutImage.objects.all()
    context = {
        'team':team,
        'imagez':imagez,
    }
    return render(request, 'about.html', context)



def sitemap(request):
    return render(request, 'sitemap.xml', content_type='text/xml')

def sitemap_index(request):
    return HttpResponse(render_to_string("custom_sitemap_index.xml", {
        'request': request
    }), content_type="application/xml")

#end
def robots(request):
    return render(request, 'robot.txt', content_type='text')


def categories(request):
    data1 =  Category.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    
    paginator = Paginator(data1, 12)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
        'data':data,
    }
    return render(request, 'categories.html', context)


def categoriesd(request, pk):
    data3 =  Category.objects.get(slug=pk)
    data1 =  Blog.objects.filter(category=data3).order_by('-id')
    data2 =  Blog.objects.filter(most_visited=True).order_by('-id')[:4]
    page = request.GET.get('page', 1)


    
    paginator = Paginator(data1, 12)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
        'data':data,
        'data3':data3,
        'data2':data2,
    }
    return render(request, 'categories_blog.html', context)



def blogs(request):
    return redirect('blog:blog')

def gallery(request):
    data1 =  Gallery.objects.all().order_by('-id')
    data2 =  Blog.objects.filter(most_visited=True).order_by('-id')[:4]
    page = request.GET.get('page', 1)


    
    paginator = Paginator(data1, 12)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
        'data':data,
        'data2':data2,
    }
    return render(request, 'gallery.html', context)



def search(request):
    if request.method == 'GET':
        q = request.GET.get('q', '').strip()
        data1 =  Blog.objects.filter(Q(h1__contains=q)| Q(content__contains=q)).order_by('-id')
        data2 =  Blog.objects.filter(most_visited=True).order_by('-id')[:4]
        page = request.GET.get('page', 1)


        
        paginator = Paginator(data1, 12)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        if data:
            pass
        else:
            data =  Blog.objects.all().order_by('-id')      
        context = {
            'data':data,
            'data1':data1,
            'data2':data2,
        }

    return render(request, 'all_blog.html', context)


def faq(request):
    
    
    context = {
    }
    return render(request, 'faq.html', context)


def privacy(request):
    context = {

    }
    return render(request, 'privacy.html', context)


def cookie(request):
    context = {

    }
    return render(request, 'cookie.html', context)

def gp(request):
    context = {

    }
    return render(request, 'guest.html', context)


def checkup(request):
    if request.method =='GET':
        name = request.GET.get('name')
        name =str(name)
        data = User.objects.filter(username=name).count()
        if data > 0:
            test = 0
        else:
            test = 1    
        
        context = {
            'test':test
        }
    return JsonResponse({'test':test})


def api_user_login(request):
    if request.method == "POST":
        # your sign in logic goes here
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            #authenticate checks if credentials exists in db
            print(username, password)
            apiurl = 'https://adesurat.com/API.php?call=login'
            apiurl = str(apiurl)
            data = {
                "username": username,
                "password": password
            }
            
            print(apiurl)
            res = requests.post(apiurl, data=data)
            dict_data = res.json()
            login_success = (dict_data['status'])
            login_success = str(login_success)
            if login_success == "True":
                token = (dict_data['token'])
                token = str(token)
                
                print(dict_data['user'])
                user = dict_data['user']
                ids = user['userid']
                ids = str(ids)
                
                pk = token
                fk = ids
                #order
                order_apiurl = 'https://adesurat.com/API.php?call=order_list_get_dr'
                order_apiurl = str(order_apiurl)

                headers = { 
                            'Accept-Language' : 'content-copied-from-myhttpheader',
                            'User-Agent':'content-copied-from-myhttpheader',
                            'Token': pk
                        }

                data = {
                    "ids": fk
                }


                
                res = requests.post(order_apiurl, headers=headers, data=data)
                dict_data = res.json()
                order_data = (dict_data['data'])
                order_key = []
                for i in order_data:
                    for key in i:
                        order_key.append(key)
                    break    

                
                #invoice
                payment_apiurl = 'https://adesurat.com/API.php?call=paymentloadData'
                payment_apiurl = str(payment_apiurl)
                res = requests.post(payment_apiurl, headers=headers, data=data)
                dict_data = res.json()
                
                payment_data = (dict_data['data'])
                
                payment_key = []
                for i in payment_data:
                    for key in i:
                        payment_key.append(key)
                    break    


                #invoice
                invoice_apiurl = 'https://adesurat.com/API.php?call=invoiceloadData'
                invoice_apiurl = str(invoice_apiurl)
                res = requests.post(invoice_apiurl, headers=headers, data=data)
                dict_data = res.json()
                
                invoice_data = (dict_data['data'])
                
                invoice_key = []
                for i in invoice_data:
                    for key in i:
                        invoice_key.append(key)
                    break    

                #statement
                statement_apiurl = 'https://adesurat.com/API.php?call=statementData'
                statement_apiurl = str(statement_apiurl)
                res = requests.post(statement_apiurl, headers=headers, data=data)
                dict_data = res.json()
                
                statement_data = (dict_data['data'])
                print(statement_data)
                statement_key = []
                for i in statement_data:
                    for key in i:
                        statement_key.append(key)
                    break    
            
                stb = dict_data['TotalBalance']

                context = {
                    'order_data':order_data,
                    'order_key':order_key,
                    'payment_data':payment_data,
                    'payment_key':payment_key,
                    'invoice_data':invoice_data,
                    'invoice_key':invoice_key,
                    'statement_data':statement_data,
                    'statement_key':statement_key,
                    'pk':pk,
                    'did':fk,
                    'user':user,
                    'stb':stb,
                }
                return render(request, 'ext_api.html', context)

                # return redirect('home:ext_api',  pk=token, fk=ids)
            else:
                messages.error(request, 'Login Failed!')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

            # user = authenticate(username=username, password=password)
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)
            #         return redirect('home:dashboard')

            #     else:
            #         return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

                    
            # else:
            #     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
    context = {
    
    }
    return render(request, 'api_login.html', context)
    


def ext_api(request, pk, fk):
    
    #order
    order_apiurl = 'https://adesurat.com/API.php?call=order_list_get_dr'
    order_apiurl = str(order_apiurl)

    headers = { 
                'Accept-Language' : 'content-copied-from-myhttpheader',
                'User-Agent':'content-copied-from-myhttpheader',
                'Token': pk
            }

    data = {
        "ids": fk
    }


    
    res = requests.post(order_apiurl, headers=headers, data=data)
    dict_data = res.json()
    order_data = (dict_data['data'])
    order_key = []
    for i in order_data:
        for key in i:
            order_key.append(key)
        break    

    
    #invoice
    payment_apiurl = 'https://adesurat.com/API.php?call=paymentloadData'
    payment_apiurl = str(payment_apiurl)
    res = requests.post(payment_apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    payment_data = (dict_data['data'])
    
    payment_key = []
    for i in payment_data:
        for key in i:
            payment_key.append(key)
        break    


    #invoice
    invoice_apiurl = 'https://adesurat.com/API.php?call=invoiceloadData'
    invoice_apiurl = str(invoice_apiurl)
    res = requests.post(invoice_apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    invoice_data = (dict_data['data'])
    
    invoice_key = []
    for i in invoice_data:
        for key in i:
            invoice_key.append(key)
        break    

    #statement
    statement_apiurl = 'https://adesurat.com/API.php?call=statementData'
    statement_apiurl = str(statement_apiurl)
    res = requests.post(statement_apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    statement_data = (dict_data['data'])
    print(statement_data)
    statement_key = []
    for i in statement_data:
        for key in i:
            statement_key.append(key)
        break    
    
    stb = dict_data['TotalBalance']
    

    context = {
        'order_data':order_data,
        'order_key':order_key,
        'payment_data':payment_data,
        'payment_key':payment_key,
        'invoice_data':invoice_data,
        'invoice_key':invoice_key,
        'statement_data':statement_data,
        'statement_key':statement_key,
        'pk':pk,
        'did':fk,
        'stb':stb,
    }
    return render(request, 'ext_api.html', context)


def api_logout(request, pk, did):
    order_apiurl = 'https://adesurat.com/API.php?call=logout'
    order_apiurl = str(order_apiurl)
    headers = { 
                'Accept-Language' : 'content-copied-from-myhttpheader',
                'User-Agent':'content-copied-from-myhttpheader',
                'Token': pk
            }

    data = {
        "did": did
    }
    return redirect('home:home')


def print_order(request):
    if request.method == 'GET':
        #order
        fk = request.GET.get('token')
        order_no = request.GET.get('orderNo')
        order_apiurl = 'https://adesurat.com/API.php?call=orderprint'
        order_apiurl = str(order_apiurl)
       
        headers = { 
                    'Accept-Language' : 'content-copied-from-myhttpheader',
                    'User-Agent':'content-copied-from-myhttpheader',
                    'Token': fk
                }

        data = {
            "order_no": order_no
        }
    
        res = requests.post(order_apiurl, headers=headers, data=data)
        dict_data = res.json()
        
        link= str(dict_data['pdf_link'])
        context ={
            'link':link
        }
        return render(request, 'pdfview.html', context)
        # return redirect('home:home')

def print_payment(request):
    if request.method=='GET':
        doctor_id = request.GET.get('doctor_id')
        if doctor_id:
            pass
        else:
            doctor_id = ""    

        receipt_no = request.GET.get('receipt_no')
        if receipt_no:
            pass
        else:
            receipt_no = ""    
        
        amount = request.GET.get('amount')
        if amount:
            pass
        else:
            amount = ""   
        
        payment_mode = request.GET.get('payment_mode')
        if payment_mode:
            pass
        else:
            payment_mode = ""   
        
        
        chq_no = request.GET.get('chq_no')
        if chq_no:
            pass
        else:
            chq_no = "" 

        date = request.GET.get('date')
        if date:
            pass
        else:
            date = "" 

        fk = request.GET.get('token')
        if fk:
            pass
        else:
            fk = "" 
        print(fk)

        #order
        apiurl = 'https://adesurat.com/API.php?call=printpayment'
        apiurl = str(apiurl)
        
        headers = { 
                    'Accept-Language' : 'content-copied-from-myhttpheader',
                    'User-Agent':'content-copied-from-myhttpheader',
                    'Token': fk
                }

        data = {
            "doctor_id": doctor_id,
            "receipt_no":receipt_no,
            "amount":amount,
            "payment_mode":payment_mode,
            "chq_no":chq_no,
            'date':date
            
        }
        print(data)
        res = requests.post(apiurl, headers=headers, data=data)
        dict_data = res.json()
        print(dict_data)
        link= str(dict_data['pdf_link'])
        context ={
            'link':link
        }
        return render(request, 'pdfview.html', context)
    
    # return redirect('home:home')

def print_statment(request, pk, did):
    #order
    apiurl = 'https://adesurat.com/API.php?call=printstatement'
    apiurl = str(apiurl)
    
    headers = { 
                'Accept-Language' : 'content-copied-from-myhttpheader',
                'User-Agent':'content-copied-from-myhttpheader',
                'Token': pk
            }

    data = {
        "doctor_id": did,
        
        
    }
    res = requests.post(apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    link= str(dict_data['pdf_link'])
    context ={
        'link':link
    }
    return render(request, 'pdfview.html', context)
    
    # return redirect('home:home')

def print_invoice(request, pk, did):
    #order
    apiurl = 'https://adesurat.com/API.php?call=printinvoice'
    apiurl = str(apiurl)
    
    headers = { 
                'Accept-Language' : 'content-copied-from-myhttpheader',
                'User-Agent':'content-copied-from-myhttpheader',
                'Token': pk
            }

    data = {
        "invoice_ids": did, 
    }
    res = requests.post(apiurl, headers=headers, data=data)
    dict_data = res.json()
    
    link= str(dict_data['pdf_link'])
    context ={
        'link':link
    }
    return render(request, 'pdfview.html', context)
    
    # return redirect('home:home')
def bdl(request):
    
    pk = Place.objects.all()
    context = { 
        'pk':pk,
    }
    return render(request, 'bdl.html', context)

# def service_view(request):
#     services = [
#         {"title" : "CAD/CAM Technology", "content": "Advance Dental Export remains the leader in offering digital technology to our clients. We currently support 3M True Definition, Cadent Itero, as well as many other open architecture systems. Contact our dedicated staff for further assistance." },
#         {"title" : "Shade Analysis", "content": " We can match the most difficult shades using your digital photos or in-lab consultation. – Send digital photos to:<a href='mailto:color@advancedentalexport.com'>color@advancedentalexport.com</a>" },
#         {"title" : "Case Planning Assistance", "content": "Personal consultations with doctors and staff for treatment options with recommendations from a technical perspective." },
#         {"title" : "Diagnostic Wax-Ups", "content": "Complete diagnostic wax-up service for treatment planning." },
#         {"title" : "Cosmetic Restoration Service", "content": " Esthetic diagnostic wax-ups, silicone matrices for intraoral mock-ups and temporaries. We use the latest materials and technologies to achieve predictable results for your patients." },
#         {"title" : "Implant Specialists", "content": "Assistance with implant cases, including diagnostic wax-up, stent fabrication and components for implant systems. In house design for custom abutments and denture bars." },
#         {"title" : "Custom Milling", "content": "Custom milling of zirconia, implant abutments, overdenture bars, temporaries and ceramics." },
#         {"title" : "Laser Welding", "content": "Laser welding for quick repairs of partial dentures" },
#     ]
#     context = { 
#         'services':services,
#     }
#     print(services)
#     return render(request, 'index.html', context)


def bdld(request, slug):
    main3 = Blog.objects.filter(main3=True).order_by('-id')[:3]
    data = Testimonials.objects.all().order_by('-id')[:20]
    data2 = Blog.objects.all().order_by('-id')[:3]
    client = Client.objects.all().order_by('-id')
    gallery = Gallery.objects.all().order_by('-id')[:7]
    gallery21 = BeforeAfter.objects.all().order_by('-id')[:5]
    video      =VideoTestimonals.objects.all().order_by('-id')[:4]
    pk = Place.objects.get(slug=slug)
    
    faq_data = [
        {
            'question': f"Which is the best dental laboratory near me in {pk.name}?",
            'answer': f"For the best dental laboratory in {pk.name}, Advance Dental Export (ADE) is a leading choice for high precision, advanced technology and quality services. We provide services all over {pk.name} and internationally as well, making it a perfect and reliable choice."
        },
        {
            'question': "How do I choose a dental lab?",
            'answer': "While choosing a dental lab, aspects like its technology, team experience, quality certifications (such as FDA registration), quality of materials used, turnaround time and customer service should be considered. The best lab can deliver superior results by understanding your clinical needs."
        },
        {
            'question': "Which dental services are provided at ADE dental laboratory?",
            'answer': "Advance Dental Export offers a wide range of dental services such as dental implant prosthetics, crowns and bridges including Zirconia and IPS E.Max, removable prosthetics (BPS denture), cosmetic dental solutions (veneers) and other specialized services."
        },
        {
            'question': "What makes our dental laboratory the best?",
            'answer': f"Factors such as advanced technology like CAD/CAM and 3D printing, a team of over 400 skilled and experienced technicians, commitment to quality with FDA registration, use of premium biocompatible materials, efficient turnaround time and close collaboration with dentists in {pk.name}."
        },
        {
            'question': f"Which dental labs in {pk.name} offer the best services?",
            'answer': f"Advance Dental Export (ADE) is at the forefront among the dental labs offering the best services in {pk.name}. With its cutting-edge technology, experienced team, quality products and collaboration with clinicians, ADE consistently delivers outstanding results."
        },
        {
            'question': "What certifications do the ADE have?",
            'answer': "Advance Dental Export (ADE) adheres to the highest standards of quality and safety and is an FDA registered laboratory. This certification demonstrates their commitment to quality."
        }
    ]
    context = { 
        'pk':pk,
        'main3':main3,
        'data':data,
        'data2':data2,
        'client':client,
        'gallery':gallery,
        'gallery21':gallery21,
        'video':video,
        'faq_data': faq_data,

    }
    if pk.type == 'city':
        template_name = 'bdld.html'
    else:
        template_name = 'state-bdlb.html'

    return render(request, template_name, context)
    
def error_404(request):
        return render(request,'404.html')

def error_500(request):
        return render(request,'500.html')

def web_story(request):
    stories = WebStory.objects.all().order_by('-publish_date')
    return render(request, 'web_story.html', {'stories': stories})

def web_story_detail(request, story_slug):
    story = get_object_or_404(WebStory, slug=story_slug)
    videos = WebStoryVideo.objects.filter(web_story=story)
    return render(request, "web_story_detail.html", {"story": story, "videos": videos, "data": story})

def sitemap(request):
    products = Product.objects.all()
    places = Place.objects.all().values('id','name','title','slug','h1')
    data1 = Blog.objects.all().order_by('-id')
    webstory = WebStory.objects.all()
    exhibition = Events.objects.all()

    context = {
        'data':data1,
        'places':places,
        'webstory':webstory,
        'products':products,
        'exhibition':exhibition
    }
    return render(request,'sitemap.html',context)

def static_sitemap(request):
    sitemap = StaticSitemap()
    items = sitemap.items()
    
    urlset = []
    for item in items:
        loc = request.build_absolute_uri(sitemap.location(item))
        url_info = {
            'location': loc,
            'lastmod': sitemap.lastmod(item) if hasattr(sitemap, 'lastmod') else None,
            'changefreq': sitemap.changefreq(item),
            'priority': sitemap.priority(item),
            'images': sitemap.image_urls(item)
        }
        urlset.append(url_info)

    xml_content = render_to_string('sitemap-static.xml', {'urlset': urlset})
    return HttpResponse(xml_content, content_type='application/xml')

def blog_sitemap(request):
    sitemap = BlogSitemap()
    items = sitemap.items()

    urlset = []
    for item in items:
        loc = request.build_absolute_uri(sitemap.location(item))
        url_info = {
            'location': loc,
            'lastmod': sitemap.lastmod(item),
            'changefreq': sitemap.changefreq(item),
            'priority': sitemap.priority(item),
            'images': sitemap.image_urls(item),
        }
        urlset.append(url_info)

    xml = render_to_string('sitemap-blog.xml', {'urlset': urlset})
    return HttpResponse(xml, content_type='application/xml')

def product_sitemap(request):
    sitemap = ProductSitemap()
    items = sitemap.items()

    urlset = []
    for item in items:
        loc = request.build_absolute_uri(sitemap.location(item))
        url_info = {
            'location': loc,
            'changefreq': sitemap.changefreq,
            'priority': sitemap.priority,
            'images': sitemap.image_urls(item),
        }
        urlset.append(url_info)

    xml = render_to_string('sitemap-products.xml', {'urlset': urlset})
    return HttpResponse(xml, content_type='application/xml')

def webstory_sitemap(request):
    sitemap = WebStorySitemap()
    items = sitemap.items()

    urlset = []
    for item in items:
        loc = request.build_absolute_uri(sitemap.location(item))
        url_info = {
            'location': loc,
            'changefreq': sitemap.changefreq(item),
            'priority': sitemap.priority(item),
            'lastmod': sitemap.lastmod(item),
            'images': sitemap.image_urls(item),
            'videos': sitemap.video_urls(item)
        }
        urlset.append(url_info)

    xml = render_to_string('sitemap-webstory.xml', {'urlset': urlset})
    return HttpResponse(xml, content_type='application/xml')

def exhibition_sitemap(request):
    sitemap = ExhibitionSitemap()
    items = sitemap.items()

    urlset = []
    for item in items:
        loc = request.build_absolute_uri(sitemap.location(item))
        url_info = {
            'location': loc,
            'changefreq': sitemap.changefreq(item),
            'priority': sitemap.priority(item),
            'images': sitemap.image_urls(item), 
        }
        urlset.append(url_info)
    xml = render_to_string('sitemap-exhibition.xml', {'urlset': urlset})
    return HttpResponse(xml, content_type='application/xml')

def bestdentallab_sitemap(request):
    sitemap = BestDentalLabSitemap()
    items = sitemap.items()

    urlset = []
    for item in items:
        loc = request.build_absolute_uri(sitemap.location(item))
        url_info = {
            'location': loc,
            'changefreq': sitemap.changefreq, 
            'priority': sitemap.priority,      
            'images': sitemap.image_urls(item),
        }
        urlset.append(url_info)

    xml = render_to_string('sitemap-bestDental.xml', {'urlset': urlset})
    return HttpResponse(xml, content_type='application/xml')

def news_sitemap(request):
    sitemap = NewsSitemap()
    items = sitemap.items()

    urlset = []
    for item in items:
        loc = request.build_absolute_uri(sitemap.location(item))
        url_info = {
            'location': loc,
            'changefreq': sitemap.changefreq,
            'priority': sitemap.priority,
            'images': sitemap.image_urls(item),
            'news': sitemap.news_metadata(item),
        }
        urlset.append(url_info)
    xml = render_to_string('sitemap-news.xml', {'urlset': urlset})
    return HttpResponse(xml, content_type='application/xml')