from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.accounts import endpoints_urls as accounts_views
from apps.address import endpoints_urls as address_endpoints_urls
from apps.admin_panel import endpoints_urls as admin_views
from apps.application_videos import endpoints_urls as application_videos_views
from apps.brochures import endpoints_urls as brochures_views
from apps.category import endpoints_urls as category_views
from apps.company_info import views as company_views
from apps.dashboard import views as dashboard_views
from apps.dashboard.urls import urlpatterns as dashboard_urls
from apps.industry_updates import endpoints_urls as industry_views
from apps.notifications import endpoints_urls as notifications_views
from apps.product import endpoints_urls as product_views
from apps.project import endpoints_urls as project_views
from apps.project_application import endpoints_urls as application_views
from apps.sellingPoint import endpoints_urls as selling_point_views
from apps.slider import endpoints_urls as slider_views
from apps.sms_notifications import endpoints_urls as sms_notifications_views
from apps.solution import endoints_urls as solution_views
from apps.supplier import endpoints_urls as supplier_views
from apps.orders import  endpoints_urls as orders_views
from apps.jop_type import  endpoints_urls as jop_type_views
from apps.offer import  endpoints_urls as offers_views
from apps.request_permissions import  endpoints_urls as request_views

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
router.register(r'SMS/modifySMSNotifications', sms_notifications_views.SMSNotificationViewSet,
                basename='CreateSMSNotification')
router.register(r'SMS/modifySMSContacts', sms_notifications_views.SMSContactsViewSet, basename='CreateSMSContact')
router.register(r'notifications/registerTokenId', notifications_views.registerTokenIds,
                basename='RegisterNotifications')
router.register(r'notifications/handleNotifications', notifications_views.handleNotifications, basename='HandleNotifications')
router.register(r'order', orders_views.OrderViewSet, basename='CreateOrder')
router.register(r'cart', orders_views.CartViewSet, basename='CreateCart')
router.register(r'jopType', jop_type_views.JobTypeViewSet, basename='CreateJopTypes')
router.register(r'offers', offers_views.OfferViewSet, basename='CreateOffers')
router.register(r'requestAccess', request_views.RequestAccessViewSet, basename='CreateRequestAccess')
admin_router.register(r'manageProducts', admin_views.ManageProductsViewSet, basename='ManageProducts')
admin_router.register(r'manageProjects', admin_views.ManageProjectsViewSet, basename='ManageProjects')
admin_router.register(r'manageSolution', admin_views.ManageSolutionViewSet, basename='ManageSolution')
admin_router.register(r'manageSellingPoints', admin_views.ManageSellingPointsViewSet, basename='ManageSellingPoints')
admin_router.register(r'manageBrochures', admin_views.ManageBrochuresViewSet, basename='ManageBrochures')
admin_router.register(r'manageOrders', admin_views.ManageOrdersViewSet, basename='ManageOrders')
admin_router.register(r'manageProductsPage', admin_views.ManageProductsPageViewSet, basename='ManageProductsPage')



urlpatterns = [

    path('api/', include(router.urls)),
    path('api/admin_panel/', include(admin_router.urls)),
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
handler404 = 'apps.handle_errors.views.error_404'
handler500 = 'apps.handle_errors.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
