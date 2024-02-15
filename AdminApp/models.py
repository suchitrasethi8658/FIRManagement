from django.contrib.auth.models import User
from django.db import models
import random

# Create your models here.
class UserProfile(models.Model):
    USER_TYPES = [
        ('Victim', 'Victim'),
        ('Police Staff', 'Police Staff'),
        ('SP', 'SP'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_details')
    profilePicture = models.ImageField(blank=True, null=True)
    DOB = models.DateField()
    contact_No = models.PositiveIntegerField()
    userType = models.CharField(max_length=20, choices= USER_TYPES, default= 'Victim')
    gender = models.CharField(max_length=10)
    adhaar_no = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.user.username


class FIR_SECTION(models.Model):
    FIR_STATUS = [
        ('Pending', 'Pending'),
        ('Waiting for Witness', 'Waiting for Witness'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    place_of_incident=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    description=models.TextField()
    incident_date = models.DateField(null=True, blank=True)
    incident_time = models.TimeField(null=True, blank=True)
    witness_name=models.CharField(max_length=255, null=True, blank=True)
    mobile_no=models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices= FIR_STATUS, default= 'Pending')
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Track_FIR(models.Model):
    
    CURRENT_STATUS = [
        ('InProgress', 'InProgress'),
        ('Waiting for Witness', 'Waiting for Witness'),
        ('Cancelled','Cancelled'),
        ('Resolved','Resolved'),
        ('Forwared to Court','Forwared to Court'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fir = models.ForeignKey(FIR_SECTION, on_delete=models.CASCADE, related_name='track_fir')
    current_status = models.CharField(max_length=50, choices= CURRENT_STATUS, default= 'InProgress')
    police_station=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fir.subject


class OTP(models.Model):
    def Otp_generator():
        return random.randint(1000,1999)

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_otp')
    otp = models.PositiveIntegerField(default=Otp_generator)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'OTP for ', self.user.username
