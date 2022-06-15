from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from Util.utils import download_file
from apps.accounts import dashboard_views as accounts_views
from apps.accounts.dashboard_views import UsersListView
from apps.accounts.forms import UserRegistrationForm, UserForm
from apps.accounts.models import User
from apps.common_code.views import AddModelView, UpdateModelView, ModelDeleteView

urlpatterns = [
    path('allUsers', staff_member_required(UsersListView.as_view(
        model=User,
        template_name="accounts/all_users.html",
        main_active_flag="users",
        active_flag="all_users",
        model_name="User",
        title="All Users"
    ), login_url="login"), name="allUsers"),
    path('addUsers', staff_member_required(AddModelView.as_view(
        model=User,
        form_class= UserRegistrationForm,
        main_active_flag="users",
        active_flag="add_users",
        reference_field_name="username",
        template_name="accounts/add_users.html",
        title="Add Users"
    ), login_url="login"), name="addUsers"),
    path('deleteUsers', staff_member_required(UsersListView.as_view(
        model=User,
        template_name="accounts/delete_users.html",
        main_active_flag="users",
        active_flag="delete_users",
        model_name="User",
        title="Delete Users"
    ), login_url="login"), name="deleteUsers"),
    path('deleteUser/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=User,
        main_active_flag="users",
        active_flag="delete_users",
        model_name='user',
        title="Delete Users",
        success_url="deleteUsers"
    ), login_url="login"), name="deleteUser"),
    path('editUser/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=User,
        form_class=UserForm,
        active_flag="edit_users",
        main_active_flag="users",
        reference_field_name="full_name",
        template_name="accounts/edit_user.html",
        title="Update User",
        # success_url="dashboard/users/allUsers"
    ), login_url="login"), name="editUser"),
    path('editUsers', staff_member_required(UsersListView.as_view(
        model=User,
        template_name="accounts/edit_users.html",
        main_active_flag="users",
        active_flag="edit_users",
        model_name="user",
        title="Update Users"
    ), login_url="login"), name="editUsers"),
    path('changePassword', accounts_views.change_password, name='changePassword'),
    path('downloadReport/<path:file_path>/<str:file_name>', download_file,name='downloadReport'),
]