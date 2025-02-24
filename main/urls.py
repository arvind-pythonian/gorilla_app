from altair.theme import names
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from main.views import RegisterView, UserView, UploadView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user'),
    path('upload/', UploadView.as_view(), name='file_upload')
]