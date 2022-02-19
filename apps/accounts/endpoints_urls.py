from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from Util.permissions import IsAnonymousUser, UnisealPermission
from Util.utils import EnablePartialUpdateMixin
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainPairSerializer


class Logout(APIView):
    def post(self, request):

        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework.response import Response
        from rest_framework import status
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ModifyUserDataViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
          API endpoint that allows to modify users' data by Admin Only
          this endpoint allows only GET,PUT,DELETE function
          permissions to this view is restricted as the following:
          - Only admin users can use GET,PUT,DELETE functions on this endpoint
          - Other types of users are not allowed to use this endpoint
          Data will be retrieved in the following format using GET function:
        {
        "id": 26,
        "username": "ali",
        "full_name": "ali hassan hamid",
        "organization": "organization_name",
         "email": "ali@gmail.com",
         "gender": "male",
         "phone_number": "0922367654",
         "city": "city_id",


    }
    Use PUT function by accessing this url:
    /accounts/modifyUsersData/<user's_id>
    Format of data will be as the previous data format for GET function
    """
    from apps.accounts.serializers import RegisterSerializer
    from .models import User
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'username', 'phone_number']

    def get_view_name(self):
        return _("Modify Users' Data")



class RegisterUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        API endpoint that allows to register new users
        this endpoint allows only POST function
        permissions to this view is restricted as the following:
        - anonymous users and system backend users (Admin and Staff )
         only can access this api to create an account
         Data will be submitted in the following format using POST function:
       {
        "id": 26,
        "username": "ali",
        "full_name": "ali hassan hamid",
        "organization": "organization_name",
        "password":"password",
        "confirm_password":"confirm_password",
        "email": "ali@gmail.com",
        "gender": "male",
        "phone_number": "922367654",
        "city":"city_id",

        }
      """
    from apps.accounts.serializers import RegisterSerializer

    def get_view_name(self):
        return _("Register New User")

    from .models import User
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousUser]


class ChangePasswordView(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
        An endpoint for changing password.
        """
    from apps.accounts.serializers import ChangePasswordSerializer

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from .models import User
        return User.objects.filter(id=self.request.user.id)

from rest_framework import generics

class ForgetPasswordView(EnablePartialUpdateMixin,mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    """
        An endpoint for changing password.
        """

    from apps.accounts.serializers import ForgetPasswordSerializer
    serializer_class = ForgetPasswordSerializer

    from apps.accounts.models import User
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)




class CurrentUserDataViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    """
      API endpoint that allows to view current user data
      this endpoint allows GET,PUT,PATCH functions
      permissions to this view is restricted as the following:
      - any user role (admin - staff - customer - seller - logistic)
       currently logged into the system can use this view to get his/her data
      Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "username": "ali",
        "full_name": "ali hassan hamid",
        "organization": "organization_name",
        "email": "ali@gmail.com",
        "gender": "male",
        "phone_number": "922367654",
        "password":"encrypted_password"
        "city":"city_id",

        }
    Use PUT function by accessing this url:
    /accounts/me/<user's_id>
    Format of data will be as the previous data format for GET function
    """
    from apps.accounts.serializers import UserSerializer
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from .models import User
        return User.objects.filter(id=self.request.user.id)

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #
    #     return self.update(request, *args, **kwargs)

    # def partial_update(self, request, *args, **kwargs):
    #     from accounts.serializers import UserSerializer
    #     serialized = UserSerializer(request.user, data=request.data, partial=True)
    #     return self.update(request, *args, **kwargs)
    # def patch(self, request, pk):
    #     from accounts.serializers import UserSerializer
    #     object = self.get_object(pk)
    #     serializer = UserSerializer(object, data=request.data,
    #                                      partial=True)  # set partial=True to update a data partially
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(code=201, data=serializer.data)

    def get_view_name(self):
        return _("Current User's Data")


class ContactUsViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows to add or modify messages by
        registered users
        this endpoint allows  GET,POST,PUT,PATCH,DELETE function
        permissions  this view is restricted as the following:
        - only admin users can access this api
         Data will be retrieved in the following format using GET function:
       {
        "id": 26,
        "phone_number": phone_number,
        "email": "email",
        "name": "name",
        "address": "address",
        "message": "message",
        "website": "website_url",
        "facebook": "facebook_url",
        "twitter": "twitter_url",
        "linkedin": "linkedin_url",
        "instagram": "instagram_url",
    }
    Use PUT function by accessing this url:
    /contactUs/<contactUsMessages's_id>
    Format of data will be as the previous data format for GET function

      """
    from apps.accounts.serializers import ContactUsSerializer

    def get_view_name(self):
        return _("Create/Modify Contact Us Message")

    from apps.accounts.models import ContactUs
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [UnisealPermission]

