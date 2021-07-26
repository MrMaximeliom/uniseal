
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):


    """
    fields should be available to any user
    full_name , phone_number ,gender,email,
    """
    # from Util.ListsOfData import CITIES_CHOICES,AREA_CHOICES

    # password2 = serializers.CharField(write_only=True, required=True, label=_('Confirm Password'))

    class Meta:
        from accounts.models import User
        model = User
        fields = (
            'id', 'username', 'full_name','organization',
            'email', 'gender', 'phone_number', 'password','city_id','working_field')

    #
    # def validate(self, attrs):
    #     if not self.partial:
    #         if attrs['password'] != attrs['password2']:
    #             raise serializers.ValidationError({"password": "Password fields didn't match."})
    #     return attrs
    #
    # def create(self, validated_data):
    #     from accounts.models import User
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         full_name=validated_data['full_name'],
    #         gender=validated_data['gender'],
    #         phone_number=validated_data['phone_number'],
    #         organization=validated_data['organization'],
    #         working_field=validated_data['working_field'],
    #         city=validated_data['city'],
    #     )
    #
    #     user.set_password(validated_data['password'])
    #
    #     user.save()
    #     return user
    #
    # def update(self, instance, validated_data):
    #
    #     instance.gender = validated_data['gender']
    #     instance.phone_number = validated_data['phone_number']
    #     instance.full_name = validated_data['full_name']
    #     instance.email = validated_data['email']
    #     instance.username = validated_data['username']
    #     instance.password =  instance.set_password(validated_data['password'])
    #     instance.organization = validated_data['organization']
    #     instance.working_field = validated_data['working_field']
    #     instance.city = validated_data['city']
    #
    #
    #     instance.save()
    #     return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        from accounts.models import User
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
    from Util.ListsOfData import GENDER_CHOICES, USERS_ROLES
    from accounts.models import User
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
    # is_artist = serializers.ChoiceField(choices=User_TYPES,required=True,label='What are you?')
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, allow_blank=False)



    class Meta:
        from accounts.models import User
        model = User
        # fields = ('username','full_name','email','password','gender','user_role','phone_number')

        fields = (
            'id', 'username', 'full_name','organization', 'password', 'password2', 'email', 'gender',
            'phone_number','city','working_field')
        extra_kwargs = {

            'username': {'required': True},

        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        from accounts.models import User
        user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                gender=validated_data['gender'],
                phone_number=validated_data['phone_number'],
                organization=validated_data['organization'],
                working_field=validated_data['working_field'],
                city=validated_data['city'],

            )

        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.gender = validated_data['gender']
        instance.phone_number = validated_data['phone_number']
        instance.full_name = validated_data['full_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.set_password(validated_data['password'])
        instance.organization = validated_data['organization']
        instance.working_field = validated_data['working_field']
        instance.city = validated_data['city']

        instance.save()
        return instance


class  ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import  ContactUs
        model =  ContactUs
        fields = "__all__"