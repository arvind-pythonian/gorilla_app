import json
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from main.decorators import request_handler
from main.models import User, Employee
from main.serializers import UserSerializer, EmployeeSerializer
from main.services import csv_to_df
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("User created")
        return Response(serializer.data)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request):
        userObj = get_object_or_404(User, email=request.user)
        logger.info("User retrieved")
        return Response({"email": userObj.email, "mobile_number": userObj.mobile_number})





class UploadView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()

    @request_handler
    def get(self, request):
        serializer = self.serializer_class(Employee.objects.all(), many=True)
        logger.info("employees retrieved")
        return Response(serializer.data)

    @staticmethod
    def create_or_update(item):
        Employee.objects.update_or_create(employee_id=item.get('employee_id'), defaults={
            'name': item.get('name'),
            'email': item.get('email'),
            'department': item.get('department'),
            'designation': item.get('designation'),
            'salary': item.get('salary'),
            'date_of_joining': item.get('date_of_joining')
        })
    @staticmethod
    def update_data(validated_data):
        objects = [Employee(employee_id=item.get('employee_id'), name=item.get('name'),
            email=item.get('email'),
            department= item.get('department'),
            designation= item.get('designation'),
            salary= item.get('salary'),
            date_of_joining= item.get('date_of_joining')
        ) for item in validated_data]
        logger.info("Starting Bulk operation")
        Employee.objects.bulk_create(
            objects,
            update_conflicts=True,
            update_fields=['name', 'email', 'date_of_joining', 'designation', 'salary',
                              'department'],
        )

    @request_handler
    def post(self, request):
        try:
            columns = ["employee_id", 'name', 'email', 'date_of_joining', 'designation', 'salary',
                              'department']
            data = csv_to_df(request.FILES.get('file_uploaded'), columns).to_json(orient='records')
            validated_data = json.loads(data)
            self.update_data(validated_data)
            logger.info("File data has been updated in to the database.")
            return Response({"data": validated_data, "message": "File Uploaded Successfully!"})
        except ValueError as err:
            logger.error(str(err))
            return Response(f"{str(err)}, please re-upload", status=400)
        except (Exception, ) as err:
            logger.error(str(err))
            return Response(str(err), status=500)


