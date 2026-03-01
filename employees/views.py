from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        employee = Employee.objects.get(user=request.user)
        data = EmployeeSerializer(employee).data
        data['is_staff'] = request.user.is_staff
        return Response(data)

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        employee_id = request.data.get('employee_id')
        department = request.data.get('department')
        position = request.data.get('position')
        phone = request.data.get('phone')
        join_date = request.data.get('join_date')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username sudah dipakai'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        employee = Employee.objects.create(
            user=user,
            name=name,
            employee_id=employee_id,
            department=department,
            position=position,
            phone=phone,
            join_date=join_date
        )
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Password lama salah'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password berhasil diubah'})

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Tidak punya akses'}, status=status.HTTP_403_FORBIDDEN)
        
        employee = self.get_object()
        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response({'error': 'Password baru wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)
        
        employee.user.set_password(new_password)
        employee.user.save()
        return Response({'message': f'Password {employee.name} berhasil direset'})