from django.contrib import admin
from .models import UserProfile,FIR_SECTION,Track_FIR
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FIR_SECTION)
admin.site.register(Track_FIR)
