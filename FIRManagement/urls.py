from django.contrib import admin
from django.urls import path
from AdminApp.views import (
    Login,
    Logout,
    Action,
    Changepass, 
    Forgotpass,
    Forgotpassuser, 
    Fir_section, 
    Lodge_fir, 
    Regd, 
    Myprofile, 
    Police_view, 
    Track_fir, 
    Track_complain, 
    EditFir,
    DeleteFir,
    Profiledata,
    UpdateProfile,
    All_user,
    All_Police_User,
    All_Victim_User,
    All_Admin_User,
    EditUser,
    ViewUser,
    Dashboard,
    DeleteUser

)
from PublicApp.views import Contact, Gallery, Index, Services
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',Login,name='login'),
    path('logout/',Logout,name='logout'),
    path('action/',Action,name='action'),
    path('changepass/',Changepass,name='changepass'),
    path('forgotpass/',Forgotpass,name='forgotpass'),
    path('forgotpass-user/',Forgotpassuser,name='forgotpass-user'),
    path('fir-section/',Fir_section,name='fir-section'),
    
    path('myprofile/',Myprofile,name='myprofile'),
    path('police-view/',Police_view,name='police-view'),
    path('track-fir/',Track_fir,name='track-fir'),
    path('track-complain/',Track_complain,name='track-complain'),
    
    path('lodge-fir/',Lodge_fir,name='lodge-fir'),
    path('edit-fir/<int:id>/',EditFir,name='edit-fir'),
    path('delete-fir/<int:id>/', DeleteFir,name='delete-fir'),

    path('contact/',Contact,name='contact'),
    path('gallery/',Gallery,name='gallery'),
    path('',Index,name='index'),
    
    path('regd/',Regd,name='regd'),
    path('services/',Services,name='services'),
    path('profiledata/',Profiledata,name='profiledata'),
    path('updateprofile/', UpdateProfile, name='updateprofile'),
    
    path('all-user/', All_user, name='all-user'),
    path('all-police-user/', All_Police_User, name='all-police-user'),
    path('all-victim-user/', All_Victim_User, name='all-victim-user'),
    path('all-admin-user/', All_Admin_User, name='all-admin-user'),
    
    path('view-user/<int:id>/', ViewUser, name='edit-user'),
    path('edit-user/<int:id>/', EditUser, name='edit-user'),
    path('delete-user/<int:id>/', DeleteUser, name='delete-user'),

    path('dashboard/', Dashboard, name='dashboard')


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'AdminApp.views.error_404'