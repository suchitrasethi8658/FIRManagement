from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail

from django.conf import settings

# Create your views here.

def Contact(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        subject = f'From Crime Management, {subject}'
        body = f'Hi Admin, \n \n Mr/Mrs/Miss {name} is trying to contact you. \n \n  email: {email} \n \n message: {message} \n\n Thanks, \n Crime Management Service'
        from_email = settings.EMAIL_HOST_USER
        to_email = ['suchitrasethi711@gmail.com']    #Place your email id here.
        send_mail(subject, body, from_email, to_email, fail_silently=True)
        sub1 = "Crime Management Service"
        body1 = "Thanks for contacting us. We will get back to you within 48 hrs."
        send_mail(sub1, body1, from_email, [email], fail_silently=True)
    return render(request,'contact.html')

def Gallery(request):
    return render(request,'gallery.html')

def Index(request):
    return render(request,'index.html')


def Services(request):
    return render(request,'services.html')