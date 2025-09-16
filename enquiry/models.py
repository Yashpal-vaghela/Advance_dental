from django.db import models



class NewsLetter(models.Model):
    email = models.CharField(max_length = 150)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email
    
   
class Review(models.Model):
    name  = models.CharField(max_length = 150)
    email = models.CharField(max_length = 150)
    message  = models.TextField()
    date = models.DateField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.email
    
class Contact(models.Model):
    name  = models.CharField(max_length = 150)
    email = models.CharField(max_length = 150)
    contact = models.CharField(max_length = 150)
    city = models.CharField(max_length = 150, blank=True, null=True)
    subject = models.CharField(max_length = 150)
    message  = models.TextField()
    date = models.DateField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} - {self.email}"

class STLFile(models.Model):
    name  = models.CharField(max_length = 150)
    contact = models.CharField(max_length = 150)
    message  = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    def files(self):
        q = STLFileData.objects.filter(stl_data=self.id)
        return q

class STLFileData(models.Model):
    files = models.FileField(upload_to="STL_FILE")
    stl_data  = models.ForeignKey(STLFile, on_delete = models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.stl_data)

class Career(models.Model):
    name = models.CharField(max_length=180, blank=True, null=True)
    contact = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class CareerFile(models.Model):
    resume = models.FileField(upload_to="Career_Files")
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="files")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Resume of {self.career.name}"
    
class InstaPost(models.Model):
    name  = models.CharField(max_length = 150)
    image  = models.ImageField(upload_to="INSTA")
    date = models.DateField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
     