from django.conf.urls.static import static
from dashboard.urls import urlpatterns as dashboard_urls
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounts import views as accounts_views
from supplier import views as supplier_views
from slider import views as slider_views
from category import views as category_views
from product import views as product_views
from project import views as project_views
from project_application import views as application_views
from company_info import views as company_views
from sellingPoint import views as selling_point_views
from brochures import views as brochures_views
from solution import views as solution_views
from admin_panel import views as admin_views
from django.conf import settings
from address import endpoints_urls as address_endpoints_urls
from dashboard import views as dashboard_views
from industry_updates import views as industry_views
from sms_notifications import views as sms_notifications_views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from application_videos import views as application_videos_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
admin_router = routers.DefaultRouter()
router.APIRootView.__name__ = 'Uniseal API'
router.register(r'accounts/signUp', accounts_views.RegisterUserViewSet, basename='CreateUser')
router.register(r'accounts/modifyUsersData', accounts_views.ModifyUserDataViewSet, basename='ModifyUser')
router.register(r'accounts/me', accounts_views.CurrentUserDataViewSet, basename='CurrentUser')
router.register(r'accounts/changePassword', accounts_views.ChangePasswordView, basename='ChangePassword')
router.register(r'supplier', supplier_views.SupplierViewSet, basename='CreateSupplier')
router.register(r'address/modifyCountry', address_endpoints_urls.CountryViewSet, basename='CreateCountry')
router.register(r'address/modifyState', address_endpoints_urls.StateViewSet, basename='CreateState')
router.register(r'address/modifyCity', address_endpoints_urls.CityViewSet, basename='CreateCity')
router.register(r'address/modifyArea', address_endpoints_urls.AreaViewSet, basename='CreateArea')
router.register(r'category', category_views.CategoryViewSet, basename='CreateCategory')
router.register(r'industryUpdates', industry_views.IndustryUpdateViewSet, basename='CreateIndustry')
router.register(r'slider', slider_views.SliderViewSet, basename='CreateSlider')
router.register(r'product/modifyProduct', product_views.ProductViewSet, basename='CreateProduct')
router.register(r'product/productImage', product_views.ProductImagesViewSet, basename='CreateProductImage')
router.register(r'applicationVideos/productAppVideo', application_videos_views.ProductApplicationVideosViewSet, basename='CreateProductApplicationVideos')
router.register(r'product/similarProduct', product_views.SimilarProductViewSet, basename='LinkSimilarProducts')
router.register(r'project/createProject', project_views.ProjectViewSet, basename='CreateProject')
router.register(r'project/projectImage', project_views.ProjectImagesViewSet, basename='CreateProjectImages')
router.register(r'project/projectVideo', project_views.ProjectVideoViewSet, basename='CreateProjectVideo')
router.register(r'project/projectSolution', project_views.ProjectSolutionViewSet, basename='CreateProjectSolution')
router.register(r'projectApplication/modifyApplications', application_views.ProjectApplicationViewSet, basename='CreateProjectApplication')
router.register(r'sellingPoint/createSellingPoint', selling_point_views.SellingPointViewSet,
                basename='CreateSellingPoint')
router.register(r'companyInfo/modifyCompanyInfo', company_views.CompanyInfoViewSet, basename='ModifyCompanyInfo')
router.register(r'brochures', brochures_views.BrochuresViewSet, basename='CreateBrochures')
router.register(r'contactUs', accounts_views.ContactUsViewSet, basename='CreateContactUsMessage')
router.register(r'solution/createSolution', solution_views.SolutionViewSet, basename='CreateSolution')
router.register(r'solution/solutionImages', solution_views.SolutionImagesViewSet, basename='CreateSolutionImages')
router.register(r'solution/solutionVideos', solution_views.SolutionVideosViewSet, basename='CreateSolutionVideo')
router.register(r'SMS/modifySMSGroups', sms_notifications_views.SMSGroupsViewSet, basename='CreateSMSGroup')
router.register(r'SMS/modifySMSNotifications', sms_notifications_views.SMSNotificationViewSet, basename='CreateSMSNotification')
router.register(r'SMS/modifySMSContacts', sms_notifications_views.SMSContactsViewSet, basename='CreateSMSContact')
admin_router.register(r'manageProducts', admin_views.ManageProductsViewSet, basename='ManageProducts')
admin_router.register(r'manageProjects', admin_views.ManageProjectsViewSet, basename='ManageProjects')
admin_router.register(r'manageSolution', admin_views.ManageSolutionViewSet, basename='ManageSolution')
admin_router.register(r'manageSellingPoints', admin_views.ManageSellingPointsViewSet, basename='ManageSellingPoints')
admin_router.register(r'manageBrochures', admin_views.ManageBrochuresViewSet, basename='MManageBrochures')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin_panel/', include(admin_router.urls)),
    path('admin/', admin.site.urls),
    path('api/accounts/forgetPassword/<int:pk>/', accounts_views.ForgetPasswordView.as_view(),name='ForgetPassword'),
    path('', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/', include(dashboard_urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/logout/', accounts_views.Logout.as_view(), name='logout'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('dashboard/images/favicon.ico'))),

]
handler404 = 'handle_errors.views.error_404'
handler500 = 'handle_errors.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
