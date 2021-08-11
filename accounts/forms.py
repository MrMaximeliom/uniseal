from accounts.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        # fields='__all__'
        fields=[
            'id', 'username', 'full_name','organization', 'email',
            'phone_number','admin']
        exclude = ('slug',)
    def create(self, validated_data):
        from accounts.models import User
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

class UserLoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email' , 'password']

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        # fields='__all__'
        fields=[
            'id', 'username', 'full_name','organization', 'email',
            'phone_number','admin','password']
        exclude = ('slug',)
    def create(self, validated_data):
        from accounts.models import User
        user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number'],
                organization=validated_data['organization'],


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


        instance.save()
        return instance