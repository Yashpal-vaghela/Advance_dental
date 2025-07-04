from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.text import slugify



class Category(models.Model):
    category = models.CharField(max_length = 156)
    primary  = models.BooleanField(default=False, null=True)
    slug = models.CharField(max_length = 1256,blank=True, null=True)
    h1 = models.CharField(max_length = 156, null=True)
    meta_description = models.CharField(max_length = 900, null=True)
    meta_title = models.CharField(max_length = 156, null=True)
    breadcrumb = models.CharField(max_length = 156, null=True)
    canonical = models.CharField(max_length = 900, default="https://advancedentalexport.com/")
    og_type = models.CharField(max_length = 156, null=True)
    og_card = models.CharField(max_length = 156, null=True)
    og_site = models.CharField(max_length = 156, null=True)
    image  = models.ImageField(upload_to="SEO", null=True)
    def tot(self):
        return Blog.objects.filter(category=self.id).count()
    
    def __str__(self):
        return self.category

class Tags(models.Model):
    tags = models.CharField(max_length = 156)
    def __str__(self):
        return self.tags    

class Author(models.Model):
    description = RichTextUploadingField()
    name = models.CharField(max_length = 156)
    position = models.CharField(max_length = 156)
    fb =models.CharField(max_length = 156,blank=True, null=True)
    insta = models.CharField(max_length = 156, blank=True, null=True)
    linkedin = models.CharField(max_length = 156, blank=True, null=True)
    image  = models.ImageField(upload_to="SEO")
    def __str__(self):
        return self.name     
               
# Create your models here.
class Blog(models.Model):
    main3 = models.BooleanField(default=False)
    most_visited = models.BooleanField(default=False)
    status  = models.BooleanField(default=True)
    page_name = models.CharField(max_length = 1256,blank=True, null=True)
    
    h1  = models.CharField(max_length = 156)
    slug =models.CharField(max_length = 1256,blank=True, null=True)
    keyword = models.CharField(max_length = 156)
    description = models.CharField(max_length = 900)
    title = models.CharField(max_length = 156)
    breadcrumb = models.CharField(max_length = 156)
    canonical = models.CharField(max_length = 900, default="https://advancedentalexport.com/")
    og_type =models.CharField(max_length = 156)
    og_card = models.CharField(max_length = 156)
    og_site = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    updated  = models.DateField(auto_now=True)
    published  = models.DateField()
    content = RichTextUploadingField()
    active = True
    edits = RichTextUploadingField( blank=True, null=True)
    schema = models.TextField( blank=True, null=True)
    category = models.ManyToManyField(Category, null=True)
    tag  = models.ManyToManyField(Tags, null=True,blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)

    def review(self):
        return Testimonials.objects.all()[:3]

    def __str__(self):
        return self.h1
    
    def get_absolute_url(self):
        return reverse('blogd', kwargs={'slug': self.slug})



class Product(models.Model):
    main = models.BooleanField(default=False)
    most_visited = models.BooleanField(default=False)
    status  = models.BooleanField(default=True)
    page_name = models.CharField(max_length = 1256, blank=True, null=True)
    category = models.ManyToManyField(Category, null=False, blank=False)
    h1  = models.CharField(max_length = 156)
    slug =models.CharField(max_length = 1256, unique=True)
    keyword = models.CharField(max_length = 156)
    description = models.CharField(max_length = 900)
    title = models.CharField(max_length = 156)
    breadcrumb = models.CharField(max_length = 156)
    canonical = models.CharField(max_length = 900, default="https://advancedentalexport.com/")
    og_type =models.CharField(max_length = 156)
    og_card = models.CharField(max_length = 156)
    og_site = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    updated  = models.DateField(auto_now=True)
    published  = models.DateField()
    content = RichTextUploadingField()
    active = True
    edits = RichTextUploadingField( blank=True, null=True)
    schema = models.TextField( blank=True, null=True)
    def sub(self):
        return SubProduct.objects.filter(product=self.id)
    
    def __str__(self):
        return self.h1

    def review(self):
        a =  Testimonials.objects.filter(product=self.id)[:3]
        return a
    
    def get_absolute_url(self):
        return reverse('productd', kwargs={'slug': self.slug})
    


class SubProduct(models.Model):
    main = models.BooleanField(default=False)
    most_visited = models.BooleanField(default=False)
    status  = models.BooleanField(default=True)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    page_name = models.CharField(max_length = 1256,blank=True, null=True)
    
    h1  = models.CharField(max_length = 156)
    slug =models.CharField(max_length = 1256,blank=True, null=True)
    keyword = models.CharField(max_length = 156)
    description = models.CharField(max_length = 900)
    title = models.CharField(max_length = 156)
    breadcrumb = models.CharField(max_length = 156)
    canonical = models.CharField(max_length = 900, default="https://thegrandindianroute.com/")
    og_type =models.CharField(max_length = 156)
    og_card = models.CharField(max_length = 156)
    og_site = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    
    schema = models.TextField( blank=True, null=True)
    updated  = models.DateField(auto_now=True)
    

    blog_banner_lg = models.ImageField(upload_to="Page Data", blank=True, null=True)
    blog_banner_sm = models.ImageField(upload_to="Page Data", blank=True, null=True)
    
    
    published  = models.DateField()
    content = RichTextUploadingField()
    active = True
    edits = RichTextUploadingField( blank=True, null=True)

    def __str__(self):
        return self.h1

class Faqpage(models.Model):   
    question = models.CharField(max_length = 1156)
    answer = RichTextUploadingField( blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    subproduct = models.ForeignKey(SubProduct, on_delete=models.CASCADE,blank=True, null=True)
    
    def __str__(self):
        return self.question
   


class MostPopularBlog(models.Model):
    blog = models.ManyToManyField(Blog)
    order  = models.IntegerField()
    def __str__(self):
        return self.order
    

class AboutPage(models.Model):
    description = models.CharField(max_length = 900)
    keyword = models.CharField(max_length = 156)
    title = models.CharField(max_length = 156)
    og_type =models.CharField(max_length = 156)
    og_card = models.CharField(max_length = 156)
    og_site = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    canonical = models.CharField(max_length = 900, default="https://website.com/")
    
    why_choose_us_img = models.ImageField(upload_to="Page Data", blank=True, null=True)
    why_choose_us_img_1 = models.ImageField(upload_to="Page Data", blank=True, null=True)
    
    schema = models.TextField( blank=True, null=True)
    def __str__(self):
        return self.title


class Team(models.Model):   
    image  = models.ImageField(upload_to="SEO")
    name = models.CharField(max_length = 156)
    position = models.CharField(max_length = 1156)
    role = models.CharField(max_length = 1256, null=True)
    schema = models.TextField( blank=True, null=True)
    def __str__(self):
        return self.name

class Testimonials(models.Model):   
    image  = models.ImageField(upload_to="SEO")
    name = models.CharField(max_length = 156)
    position = models.CharField(max_length = 156)
    review = models.TextField()
    product =  models.ManyToManyField(Product, blank=True, null=True)
    
    schema = models.TextField( blank=True, null=True)
    def __str__(self):
        return self.name
   
class VideoTestimonals(models.Model):   
    name = models.CharField(max_length = 156)
    position = models.CharField(max_length = 156, default="Dentist")
    link =  models.CharField(max_length = 1256, blank=True, null=True)
    def __str__(self):
        return self.name
      
    
class Events(models.Model):   
    name = models.CharField(max_length = 156)
    slug =models.CharField(max_length = 1256,blank=True, null=True)
    image  = models.ImageField(upload_to="SEO", blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class EventsGallery(models.Model):   
    name = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    category = models.ForeignKey(Events, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class NewEventLink(models.Model):
    name = models.CharField(max_length = 156)
    city = models.CharField(max_length = 156)
    start_date = models.DateField()
    end_date = models.DateField()
    cover_image = models.ImageField(upload_to = "thumbnails/", blank=True, null=True)
    social_links = models.URLField(blank=False, null=False)
    skyline_image = models.ImageField(upload_to = "thumbnails/", blank=True, null=True)

    def __str__(self):
        return self.name

class AboutImage(models.Model):   
    name = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    
    def __str__(self):
        return self.name



class Client(models.Model):   
    name = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    
    def __str__(self):
        return self.name


class Gallery(models.Model):   
    name = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    
    def __str__(self):
        return self.name



class BeforeAfter(models.Model):   
    name = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    
    def __str__(self):
        return self.name
        
class Place(models.Model):
    name = models.CharField(max_length = 156)
    h1  = models.CharField(max_length = 156,blank=True, null=True)
    slug =models.CharField(max_length = 1256,blank=True, null=True)
    keyword = models.CharField(max_length = 156,blank=True, null=True)
    description = models.CharField(max_length = 900,blank=True, null=True)
    title = models.CharField(max_length = 156,blank=True, null=True)
    breadcrumb = models.CharField(max_length = 156,blank=True, null=True)
    canonical = models.CharField(max_length = 900, blank=True, null=True)
    og_type =models.CharField(max_length = 156,blank=True, null=True)
    og_card = models.CharField(max_length = 156,blank=True, null=True)
    og_site = models.CharField(max_length = 156,blank=True, null=True)
    image  = models.ImageField(upload_to="SEO",blank=True, null=True)
    schema = models.TextField( blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name   
        
class ContactDetails(models.Model):
    department = models.CharField(max_length = 200)
    name = models.CharField(max_length = 156)
    contact = models.CharField(max_length = 156)
    order= models.IntegerField(default= 2)
    
    def __str__(self):
        return self.name  

class WebStory(models.Model):
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    canonical_link = models.URLField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to="SEO/images/")
    links = models.URLField(blank=True, null=True)  
    author = models.CharField(max_length=100)  
    publish_date = models.DateField()  

    def __str__(self):
        return self.title         

class WebStoryVideo(models.Model):
    web_story = models.ForeignKey(WebStory, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="SEO/videos/")

    def __str__(self):
        return f"Video for {self.web_story.title}"
