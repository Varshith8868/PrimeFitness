from django.contrib import admin
from .models import Workout, UserProfile, CustomUser

admin.site.register(Workout)
admin.site.register(UserProfile)
admin.site.register(CustomUser)

