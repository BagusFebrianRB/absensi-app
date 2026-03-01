from django.test import TestCase
from django.contrib.auth.models import User
from employees.models import Employee
from attendance.models import Attendance, LeaveRequest
from django.utils import timezone

class AttendanceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123', is_staff=False)
        self.admin = User.objects.create_user(username='testadmin', password='admin123', is_staff=True)
        self.employee = Employee.objects.create(
            user=self.user,
            name='Test User',
            employee_id='EMP001',
            department='IT',
            position='Developer',
            phone='08123456789',
            join_date='2024-01-01'
        )

    def test_employee_created(self):
        self.assertEqual(self.employee.name, 'Test User')
        self.assertTrue(self.employee.is_active)

    def test_attendance_check_in(self):
        attendance = Attendance.objects.create(
            employee=self.employee,
            date=timezone.now().date(),
            check_in=timezone.now().time(),
            status='hadir'
        )
        self.assertEqual(attendance.status, 'hadir')
        self.assertIsNotNone(attendance.check_in)

    def test_attendance_alpha(self):
        attendance = Attendance.objects.create(
            employee=self.employee,
            date=timezone.now().date(),
            status='alpha'
        )
        self.assertEqual(attendance.status, 'alpha')
        self.assertIsNone(attendance.check_in)

    def test_leave_request_created(self):
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            type='izin',
            start_date='2026-03-01',
            end_date='2026-03-02',
            reason='Keperluan keluarga',
            status='pending'
        )
        self.assertEqual(leave.status, 'pending')
        self.assertEqual(leave.type, 'izin')

    def test_leave_request_approved(self):
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            type='sakit',
            start_date='2026-03-01',
            end_date='2026-03-02',
            reason='Demam',
            status='pending'
        )
        leave.status = 'approved'
        leave.save()
        self.assertEqual(leave.status, 'approved')

    def test_mark_alpha_task(self):
        from attendance.tasks import mark_alpha
        mark_alpha()
        attendance = Attendance.objects.filter(employee=self.employee, date=timezone.now().date()).first()
        self.assertIsNotNone(attendance)
        self.assertEqual(attendance.status, 'alpha')
