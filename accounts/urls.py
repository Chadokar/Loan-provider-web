from django.urls import path
from .views import RegisterUserView, GetUserDetailsView, CheckEligibility


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('check-eligibility/', CheckEligibility.as_view(), name='checkeligibility'),
    path('get_user/<int:id>/', GetUserDetailsView.as_view(),
         name='get_user_details'),
]
