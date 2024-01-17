from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoanRequestSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import status
from .models import User


class GetUserDetailsView(APIView):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user_data = request.data
        # print('user data : ', user_data)
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            account = serializer.save()
            user = serializer.data
            print(user['id'])
            return Response({
                'id': user['id'],
                # 'email': user['email'],
                'name': user['first_name'] + ' ' + user['last_name'],
                'phone_number': user['phone_number'],
                'monthly_salary': user['monthly_salary'],
                'approved_limit': user['approved_limit'],
                'success': True
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckEligibility(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            response_data = self.process_loan_request(
                serializer.validated_data)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_loan_request(self, data):
        approval = True
        interest_rate = data['interest_rate']
        corrected_interest_rate = interest_rate
        tenure = data['tenure']
        monthly_installment = self.calculate_monthly_installment(
            data['loan_amount'], interest_rate, tenure)

        response_data = {
            'customer_id': data['customer_id'],
            'approval': approval,
            'interest_rate': interest_rate,
            'corrected_interest_rate': corrected_interest_rate,
            'tenure': tenure,
            'monthly_installment': monthly_installment,
        }

        return response_data

    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        # Monthly Installment = P * [r(1+r)^n] / [(1+r)^n-1]
        r = interest_rate / 1200.0  # Monthly interest rate
        n = tenure * 12  # Total number of payments
        monthly_installment = loan_amount * (r * (1 + r)**n) / ((1 + r)**n - 1)
        return monthly_installment
