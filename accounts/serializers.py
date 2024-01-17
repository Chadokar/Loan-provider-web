from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'age',
                  'last_name', 'last_login', 'monthly_salary', 'phone_number', 'approved_limit', 'date_joined', 'is_active', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Password do not match")
        # return super().validate(attrs)
        if not attrs.get('first_name', ''):
            raise serializers.ValidationError(
                {'title': 'This field is required'})
        return attrs

    def create(self, validated_data):

        user = User.objects.create_user(
            # email=validated_data['email'],
            id=validated_data.get('id'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            age=validated_data.get('age'),
            password=validated_data.get('password'),
            monthly_salary=validated_data.get('monthly_salary'),
            approved_limit=validated_data.get('monthly_salary')*3,
            phone_number=validated_data.get('phone_number')
        )
        # print(f"creater user : ", {user})
        # return super().create(validated_data)
        return user


class LoanRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()
