from django import forms
from django.contrib.auth import authenticate

from apps.accounts.models import User

"""
UserForm class:
this class is used to create new instances of the user model
"""
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
        instance.organization = validated_data['organization']


        instance.save()
        return instance
from django.contrib.auth.forms import AuthenticationForm
"""
UserLoginForm class:
this class is used in the process of logging the user in
"""
class UserLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # altered_username = ''
        if username is not None and password:
            # # check if phone number starts with 0 or not
            # if username.startswith("0"):
            #     # remove the leading 0
            #     username = username[1:]

            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                print("user is none")
                print("username: ",username)
                print("password: ",password)

                raise self.get_invalid_login_error()

            else:
                print("user is not none")
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    class Meta:
        model=User
        fields=['phone_number' , 'password']

"""
UserRegistrationForm class:
this class is used in the process of registering new users
"""
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        # list all required fields in the User model
        fields=[
            'id', 'username', 'full_name','organization', 'email',
            'phone_number','staff','password','job_type']
        exclude = ('slug',)
    # this method is used to create new instances
    def create(self, validated_data):
        from apps.accounts.models import User
        # create new user instance from the form's fields
        user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                organization=validated_data['organization'],
                staff = validated_data['staff']
            )
        # set user's password
        user.set_password(validated_data['password'])
        # save the user
        user.save()
        # return the newly created user instance
        return user
    # this method id used to update the user's data
    def update(self, instance, validated_data):
        # get the form's fields data for each user's fields
        instance.phone_number = validated_data['phone_number']
        instance.full_name = validated_data['full_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.set_password(validated_data['password'])
        instance.organization = validated_data['organization']
        instance.staff = validated_data['staff']
        # save the instance
        instance.save()
        # return the instance
        return instance