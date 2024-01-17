# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from math import ceil
from .models import Loans
from .serializers import LoansSerializer


class ViewLoan(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        customer_id = kwargs.get('customer_id')

        if id:
            try:
                loan = Loans.objects.get(id=id)
                serializer = LoansSerializer(loan)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Loans.DoesNotExist:
                return Response({'error': 'Loan Not Found'}, status=status.HTTP_404_NOT_FOUND)

        elif customer_id:
            try:
                loans = Loans.objects.filter(customer_id=customer_id)
                data = []
                if not loans:
                    return Response({'error': 'No Loans Found for the given customer_id'}, status=status.HTTP_404_NOT_FOUND)
                for loan in loans:
                    data.append({
                        'loan_id': loan.id,
                        'loan_amount': loan.loan_amount,
                        'interest_rate': loan.interest_rate,
                        'monthly_installment': loan.monthly_installment,
                        'repayments_left': loan.repayments_left,
                    })

                return Response(data, status=status.HTTP_200_OK)
            except Loans.DoesNotExist:
                return Response({'error': 'No Loans Found for the given customer_id'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, customer_id):
        try:
            loans = Loans.objects.filter(customer_id=customer_id)

            for loan in loans:
                # Assuming received the updated repayments_left value in the request data
                new_repayments_left = request.data.get('repayments_left', None)

                if new_repayments_left is not None:
                    loan.repayments_left = new_repayments_left
                    loan.save()

            return Response({'message': 'Repayments_left updated successfully'}, status=status.HTTP_200_OK)
        except Loans.DoesNotExist:
            return Response({'error': 'No Loans Found for the given customer_id'}, status=status.HTTP_404_NOT_FOUND)


class CreateLoan(APIView):
    def post(self, request, format=None):
        try:
            data = {
                ** request.data,
                "monthly_installment": ceil(self.calculate_monthly_installment(request.data))
            }
            serializer = LoansSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"loan": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=400)

    def calculate_monthly_installment(self, data):
        if data["loan_amount"] <= 50000:
            raise ValidationError(
                detail="Loan not approved. Requested amount too low.")
        # logic to calculate monthly_installment based on loan_amount, interest_rate, and tenure
        monthly_interest_rate = data["interest_rate"] / 12 / 100
        numerator = data["loan_amount"] * monthly_interest_rate
        denominator = 1 - (1 + monthly_interest_rate) ** (- data["tenure"])
        return numerator / denominator
