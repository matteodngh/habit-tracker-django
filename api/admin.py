from django.contrib import admin
from .models import Habit, DailyCheck

admin.site.register(Habit)
admin.site.register(DailyCheck)