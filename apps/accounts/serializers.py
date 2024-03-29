from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        data.update({'user': self.user.username})
        data.update({'id': self.user.id})

        return data

class UserOrderSerializer(serializers.ModelSerializer):

    class Meta:
        from apps.accounts.models import User
        model = User
        fields = (
            'id', 'username', 'full_name')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        from apps.accounts.models import User
        model = User
        fields = (
            'id', 'username', 'full_name','organization',
            'email', 'phone_number', 'password','job_type')

class ForgetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField( required=True, validators=[validate_password],label=_('New Password'))
    password2 = serializers.CharField(write_only=True, required=True,label=_('Confirm Password'))

    class Meta:
        from apps.accounts.models import User
        model = User
        fields = ( 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs



    def update(self, instance, validated_data):
        print("setting new password: ",validated_data['password'])

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        from apps.accounts.models import User
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class RegisterSerializer(serializers.ModelSerializer):
    from rest_framework.validators import UniqueValidator
    from django.core.validators import RegexValidator
    from apps.accounts.models import User
    email = serializers.EmailField(
        required=True,

        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_regex = RegexValidator(regex=r'^9\d{8}$|^1\d{8}$',
                                 message=_("Phone number must start with 9 or 1 and includes 9 numbers."))
    phone_number = serializers.CharField(
        validators=[phone_regex,
                    UniqueValidator(queryset=User.objects.all())
                    ],
        label=_('Phone Number')
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label=_('Confirm Password'))



    class Meta:
        from apps.accounts.models import User
        model = User

        fields = (
            'id', 'username', 'full_name','organization', 'password', 'password2', 'email',
            'phone_number','job_type')
        extra_kwargs = {

            'username': {'required': True},

        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        from apps.accounts.models import User
        user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                organization=validated_data['organization'],
                job_type=validated_data['job_type'],

            )

        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.phone_number = validated_data['phone_number']
        instance.full_name = validated_data['full_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.set_password(validated_data['password'])
        instance.organization = validated_data['organization']
        instance.job_type = validated_data['job_type']

        instance.save()
        return instance


class  ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  ContactUs
        model =  ContactUs
        fields = "__all__"