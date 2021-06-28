# from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework import mixins
from uniseal.permissions import IsAdminOrReadOnly,IsSystemBackEndUser, IsAnonymousUser
# Create your views here.

class ModifyUserDataViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
          API endpoint that allows to modify users' data by Admin Only
          this endpoint allows only GET,PUT,DELETE function
          permissions to this view is restricted as the following:
          - Only admin users can use GET,PUT,DELETE functions on this endpoint
          - Other types of users are not allowed to use this endpoint
        """
    from uniseal.serializers import RegisterSerializer
    from .models import User
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsSystemBackEndUser]

    def get_view_name(self):
        return _("Modify Users' Data")


class RegisterUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        API endpoint that allows to register new users
        this endpoint allows only POST function
        permissions to this view is restricted as the following:
        - anonymous users and system backend users (Admin and Staff )
         only can access this api to create an account
      """
    from uniseal.serializers import RegisterSerializer

    def get_view_name(self):
        return _("Register New User")

    from .models import User
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymousUser]


class CurrentUserDataViewSet(viewsets.GenericViewSet,
                             mixins.RetrieveModelMixin,

                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin):
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
        "email": "ali@gmail.com",
        "gender": "male",
        "user_role": 1,
        "phone_number": "0922367654"
    }
    Use PUT function by accessing this url:
    /account/me/<user's_id>
    Format of data will be as the previous data format for GET function
    """
    from uniseal.serializers import UserSerializer
    serializer_class = UserSerializer

    # permission_classes = [permissions.IsAuthenticated]
    # http_method_names = ['get']

    def get_queryset(self):
        from .models import User
        return User.objects.filter(id=self.request.user.id)

    def get_view_name(self):
        return _("Current User's Data")
