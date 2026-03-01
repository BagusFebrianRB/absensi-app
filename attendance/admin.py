from django.contrib import admin
from .models import Attendance, LeaveRequest

admin.site.register(Attendance)
admin.site.register(LeaveRequest)