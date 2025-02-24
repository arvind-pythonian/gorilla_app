from rest_framework import serializers
from .models import User, Employee

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name","mobile_number","password"]

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                       username=validated_data['username'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   mobile_number=validated_data['mobile_number']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user

class EmployeeListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        employees = [Employee.objects.update_or_create(employee_id=item.get('employee_id'), defaults={
              'name': item.get('name'),
              'email': item.get('email'),
              'department': item.get('department'),
              'designation': item.get('designation'),
              'salary': item.get('salary'),
              'date_of_joining': item.get('date_of_joining')
              }) for item in validated_data]
        return Employee.objects.bulk_create(employees, update_conflicts=True)

class EmployeeSerializer(serializers.ModelSerializer):
    date_of_joining = serializers.DateField(format="%d-%m-%Y")
    class Meta:
        list_serializer_class = EmployeeListSerializer
        model = Employee
        fields = ["employee_id", 'name', 'email', 'date_of_joining', 'designation', 'salary',
                              'department']


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']