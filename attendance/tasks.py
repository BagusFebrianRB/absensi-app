from django.utils import timezone
from employees.models import Employee
from .models import Attendance

def mark_alpha():
    today = timezone.now().date()
    
    # Skip weekend (5=Sabtu, 6=Minggu)
    if today.weekday() >= 5:
        return
    
    employees = Employee.objects.filter(is_active=True, user__is_staff=False)
    
    for employee in employees:
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={'status': 'alpha'}
        )
        # Kalau sudah ada tapi belum check in, tandai alpha
        if not created and not attendance.check_in:
            attendance.status = 'alpha'
            attendance.save()