from django import forms
from django.contrib.auth import authenticate

from apps.accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        # fields='__all__'
        fields=[
            'id', 'username', 'full_name','organization', 'email',
            'phone_number','admin','job_type']
        exclude = ('slug',)
    def create(self, validated_data):
        from apps.accounts.models import User
        user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                organization=validated_data['organization'],

            )

        # user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.phone_number = validated_data['phone_number']
        instance.full_name = validated_data['full_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        # instance.set_password(validated_data['password'])
        instance.organization = validated_data['organization']


        instance.save()
        return instance
from django.contrib.auth.forms import AuthenticationForm
class UserLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # altered_username = ''
        if username is not None and password:
            # check if phone number starts with 0 or not
            if username.startswith("0"):
                # remove the leading 0
                username = username[1:]

            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    class Meta:
        model=User
        fields=['phone_number' , 'password']

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        # fields='__all__'
        fields=[
            'id', 'username', 'full_name','organization', 'email',
            'phone_number','staff','password','job_type']
        exclude = ('slug',)
    def create(self, validated_data):
        from apps.accounts.models import User
        user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                organization=validated_data['organization'],
                staff = validated_data['staff']
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
        instance.staff = validated_data['staff']

        instance.save()
        return instance