# urls.py
from django.urls import path
from .views import CreateLoan, ViewLoan

urlpatterns = [
    path('create-loan/', CreateLoan.as_view(), name='createloan'),
    path('view-loan/<int:id>/', ViewLoan.as_view(),
         name='view loan by id'),
    path('view-loans/<int:customer_id>/', ViewLoan.as_view(),
         name='view loans by customer_id'),
    path('update-repayments/<int:customer_id>/',
         ViewLoan.as_view(), name='update repayments'),
]
