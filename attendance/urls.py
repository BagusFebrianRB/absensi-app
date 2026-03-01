from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, LeaveRequestViewSet, export_attendance_excel, rekap_per_karyawan, export_rekap_excel, export_employees_excel

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('export/attendance/', export_attendance_excel, name='export_attendance'),
    path('export/rekap/', export_rekap_excel, name='export_rekap'),
    path('export/employees/', export_employees_excel, name='export_employees'),
    path('rekap/', rekap_per_karyawan, name='rekap_per_karyawan'),
]