from accounts.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        # fields='__all__'
        fields=[
            'id', 'username', 'full_name','organization', 'email', 'gender',
            'phone_number','city','working_field','admin','working']
        exclude = ('slug',)
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

        # user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.gender = validated_data['gender']
        instance.phone_number = validated_data['phone_number']
        instance.full_name = validated_data['full_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        # instance.set_password(validated_data['password'])
        instance.organization = validated_data['organization']
        instance.working_field = validated_data['working_field']
        instance.city = validated_data['city']

        instance.save()
        return instance

class UserLoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email' , 'password']