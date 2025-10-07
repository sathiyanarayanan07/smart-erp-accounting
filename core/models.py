from django.db import models


class user (models.Model):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    First_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=255,blank=True,null=True)
    password = models.CharField(max_length=255,blank=True,null=True)
    otp = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f"{self.First_name},{self.last_name}"
    



    


    

