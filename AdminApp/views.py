from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, OTP, FIR_SECTION, Track_FIR
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

import random
# Create your views here.

def Login(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    msg=""
    if request.method == "POST":
        user = request.POST["username"]
        password = request.POST["password"]
        data = authenticate(username=user, password=password)
        if data != None:
            login(request, data)
            return redirect("profiledata")
        msg='Incorrect username or password'
    return render(request, 'login.html',{'msg':msg})


def Logout(request):
    logout(request)
    return redirect("index")


def Regd(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        DOB = request.POST.get('DOB')
        profile_pic = request.FILES.get('profile_pic')
        Adhaar_no = request.POST.get('adhaar_no')
        gender= request.POST.get('gender')
        usertype= request.POST.get('usertype')
        
        if pass1 != pass2:
            message = 'Password should be same !'
            return render(request, 'regd.html', {'message': message})
        
        if len(contact) != 10:
            message = 'Contact should be 10 digit only.'
            return render(request, 'regd.html', {'message': message})
        try:
            u = User.objects.create_user(
                username=username, email=email, password=pass1, first_name=first_name, last_name=last_name)
        except:
            message = 'User name already exists!'
            return render(request, 'regd.html', {'message': message})
        UserProfile.objects.create(
            user=u, contact_No=contact, DOB=DOB, profilePicture=profile_pic, userType=usertype, gender=gender, adhaar_no=Adhaar_no)

        return redirect('login')

    return render(request, 'regd.html')

def Action(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'action.html')


def Changepass(request):
    if not request.user.is_authenticated:
        return redirect('login')
    message = ''
    if request.method == 'POST':
        oldpass = request.POST.get('oldpass')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            message = 'Password should be same !'
            return render(request, 'changepass.html', {'message': message})
        try:
            u = User.objects.get(username=request.user.username)
        except:
            message = 'Please enter correct User Name!'
            return render(request, 'changepass.html', {'message': message})

        check = u.check_password(oldpass)
        if check:
            u.set_password(pass1)
            u.save()
            data = authenticate(username=u.username, password=pass1)
            if data != None:
                login(request, data)
            return redirect("profiledata")
        message = 'Please enter valid Old password!'
        return render(request, 'changepass.html', {'message': message})
    return render(request,'changepass.html')


def Forgotpassuser(request):
    message = ''
    if request.method == 'POST':
        uname = request.POST.get('username')
        try:
            u = User.objects.get(username=uname)
        except:
            message = 'Username doesnot exit.'
            return render(request,'forgotpass-user.html',{'message': message})
        try:
            to_email = [u.email]
        except:
            message = 'Email is not valid.'
            return render(request,'forgotpass-user.html',{'message': message})
        
        otp= OTP.objects.create(user=u)
        subject = 'OTP FOR CRIME MANAGEMENT USER'
        body = f'Hi,{u.username} Your OTP for forgot password is {otp.otp}'
        from_email = settings.EMAIL_HOST_USER
       
        send_mail(subject,body,from_email,to_email, fail_silently=True)
        return redirect('forgotpass')
    return render(request,'forgotpass-user.html')


def Forgotpass(request):
    message = ''
    if request.method == 'POST':
        otp = request.POST.get('otp')
        uname = request.POST.get('uname')
        newpassword1 = request.POST.get('newpassword1')
        newpassword2 = request.POST.get('newpassword2')
        if newpassword1 != newpassword2:
            message = 'Password should be same !'
            return render(request, 'forgotpass.html', {'message': message})
        try:
            u = User.objects.get(username=uname)
        except:
            message = 'Please enter correct User Name!'
            return render(request, 'forgotpass.html', {'message': message})
        u_otp=OTP.objects.filter(user=u).order_by('-created_at').first()
        print(type(u_otp.otp),type(otp))
        if str(u_otp.otp) == otp:
            u.set_password(newpassword1)
            u.save()
            return redirect('login')
        message = 'Please provide valid OTP'
        return render(request, 'forgotpass.html', {'message': message})
    return render(request,'forgotpass.html')


def Fir_section(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'fir-section.html')


def Lodge_fir(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        incident_date = request.POST.get('incident_date')
        incident_time = request.POST.get('incident_time')
        place_of_incident = request.POST.get('place_of_incident')
        mobile_no = request.POST.get('mobile_no')
        eye_witness_name = request.POST.get('eye_witness_name')
        police_station = request.POST.get('police_station')

        if len(mobile_no) != 10:
            msg="Please provide valid phone number"
            return render(request,'lodge-fir.html', {'msg':msg})
        
        f = FIR_SECTION.objects.create(
            user=UserProfile.objects.get(user=request.user),
            subject=subject,
            place_of_incident =  place_of_incident,
            category = category,
            description = description,
            incident_date = incident_date,
            incident_time = incident_time,
            witness_name = eye_witness_name,
            mobile_no = mobile_no
        )
        Track_FIR.objects.create(
            user=UserProfile.objects.get(user=request.user),
            fir=f,
            police_station = police_station
        )
        return redirect('track-fir')
    return render(request,'lodge-fir.html')


def Myprofile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        username = request.user.username
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        addhar = request.POST.get('addhar')
        pic = request.FILES.get('pic')
        
        if len(contact) != 10:
            msg = 'Phone Number should be 10 digit only.'
            return render(request,'myprofile.html', {'msg':msg})
        
        u = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=u)
        u.first_name=first_name
        u.last_name=last_name
        u.email=email
        user_profile.contact_No=contact
        user_profile.adhaar_no=addhar
        user_profile.DOB=dob
        if pic:
            user_profile.profilePicture=pic

        u.save()
        user_profile.save()
        return redirect('profiledata')
    return render(request,'myprofile.html')


def Police_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'police-view.html')

def Track_fir(request):
    if not request.user.is_authenticated:
        return redirect('login')
    up = UserProfile.objects.get(user=request.user)
    if up.userType == "Police Staff":
        ta = Track_FIR.objects.exclude(Q(current_status="Resolved") | Q(current_status="Cancelled")).order_by('-id')
    elif up.userType == "SP":
        ta = Track_FIR.objects.all().order_by('-id')
    else:
        ta = Track_FIR.objects.filter(user=up).order_by('-id')
    
    
    page = request.GET.get('page', 1)

    paginator = Paginator(ta, 10)
    try:
        t = paginator.page(page)
    except PageNotAnInteger:
        t = paginator.page(1)
    except EmptyPage:
        t = paginator.page(paginator.num_pages)
    
    Dict = {
        'track': t
    }
    return render(request,'track-fir.html', Dict)

def Track_complain(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'track-complain.html')


def EditFir(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    track_fir = Track_FIR.objects.get(id=id)
    choices = Track_FIR.CURRENT_STATUS
    choice = []
    for c in choices:
        if c[0] != track_fir.current_status:
            choice.append(c[0])
        else:
            continue
    
    if request.method == "POST":
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        incident_date = request.POST.get('incident_date')
        incident_time = request.POST.get('incident_time')
        place_of_incident = request.POST.get('place_of_incident')
        mobile_no = request.POST.get('mobile_no')
        eye_witness_name = request.POST.get('eye_witness_name')
        police_station = request.POST.get('police_station')
        status = request.POST.get('status')

        if len(mobile_no) != 10:
            msg="Please provide valid phone number"
            return render(request,'edit-lodge-fir.html', {'msg':msg})
        
        if status:
            track_fir.current_status = status
            subject = 'CRIME MANAGEMENT SUPPORT'
            body = f'Hi,{track_fir.user.user.first_name},\n\n Your FIR Status has beend changed to {status}. \n\n Thanks,\nSupport Team'
            from_email = settings.EMAIL_HOST_USER
            to_email = [track_fir.user.user.email]
        
            send_mail(subject,body,from_email,to_email, fail_silently=True)
        track_fir.fir.category = category
        track_fir.fir.subject = subject
        track_fir.fir.place_of_incident = place_of_incident
        track_fir.fir.description = description
        track_fir.fir.incident_time = incident_time
        track_fir.fir.incident_date = incident_date
        track_fir.fir.witness_name = eye_witness_name
        track_fir.fir.mobile_no = mobile_no
        track_fir.police_station = police_station
        track_fir.fir.save()
        track_fir.save()
        return redirect('track-fir')

    return render(request,'edit-lodge-fir.html', {'details':track_fir, 'choice':choice})


def DeleteFir(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    fir = FIR_SECTION.objects.get(id=id)
    fir.delete()
    return redirect('track-fir')


def Profiledata(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'profiledata.html')

def UpdateProfile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        username = request.user.username
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        pic = request.FILES.get('pic')

        u = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=u)
        u.first_name=first_name
        u.last_name=last_name
        u.email=email
        user_profile.contact_No=contact
        user_profile.DOB=dob
        user_profile.profilePicture=pic

        u.save()
        user_profile.save()
        return redirect('profiledata')
    return render(request,'myprofile.html')

def All_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = UserProfile.objects.exclude(user=request.user)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    Dict = {"users":users}
    return render(request,'users.html', Dict)



def All_Police_User(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = UserProfile.objects.filter(userType="Police Staff").exclude(user=request.user)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    Dict = {"users":users}
    return render(request,'users.html', Dict)




def All_Victim_User(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = UserProfile.objects.filter(userType="Victim").exclude(user=request.user)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    Dict = {"users":users}
    return render(request,'users.html', Dict)


def All_Admin_User(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = UserProfile.objects.filter(userType="SP").exclude(user=request.user)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    Dict = {"users":users}
    return render(request,'users.html', Dict)


def EditUser(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_profile = UserProfile.objects.get(id=id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        addhar = request.POST.get('addhar')
        pic = request.FILES.get('pic')
        
        if len(contact) != 10:
            msg = 'Phone Number should be 10 digit only.'
            return render(request,'edit-user.html', {'details':user_profile, 'msg':msg})
        
        user_profile.user.first_name=first_name
        user_profile.user.last_name=last_name
        user_profile.user.email=email
        user_profile.contact_No=contact
        user_profile.adhaar_no=addhar
        user_profile.DOB=dob
        if pic:
            user_profile.profilePicture=pic
        user_profile.user.save()
        user_profile.save()
        return redirect('all-user')
    
    return render(request,'edit-user.html', {'details':user_profile})

def DeleteUser(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_profile = UserProfile.objects.get(id=id)

    user = User.objects.get(username=user_profile.user.username)

    user.delete()
    return redirect('all-user')


def ViewUser(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_profile = UserProfile.objects.get(id=id)
    return render(request,'view-user.html', {'details':user_profile})


def Dashboard(request):
    victim_data = Track_FIR.objects.filter(user=UserProfile.objects.get(user=request.user)).count()
    victim_resolved_data = Track_FIR.objects.filter(Q(current_status="Resolved") | Q(current_status="Cancelled"), user=UserProfile.objects.get(user=request.user)).count()
    victim_progress_data = Track_FIR.objects.filter(Q(current_status="InProgress") | Q(current_status="Waiting for Witness") |Q(current_status="Forwared to Court"), user=UserProfile.objects.get(user=request.user)).count()
    all_track = Track_FIR.objects.all().count()
    resolved_track = Track_FIR.objects.filter(current_status="Resolved").count()
    in_progress_track = Track_FIR.objects.filter(current_status="InProgress").count()
    ForwaredtoCourt = Track_FIR.objects.filter(current_status="Forwared to Court").count()
    Waiting = Track_FIR.objects.filter(current_status="Waiting for Witness").count()
    Cancelled = Track_FIR.objects.filter(current_status="Cancelled").count()

    Dict = {
        'all_track':all_track,
        'resolved_track':resolved_track,
        'pending_track':in_progress_track,
        'Forwared_to_Court':ForwaredtoCourt,
        'Waiting_for_Witness':Waiting,
        'Cancelled':Cancelled,
        'victim_data': victim_data,
        'victim_resolved_data':victim_resolved_data,
        'victim_progress_data':victim_progress_data
    }
    return render(request, 'dashboard.html', Dict)



def error_404(request, exception):
    return render(request,'404.html')