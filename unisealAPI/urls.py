from django.conf.urls.static import static
from product.urls import urlpatterns as product_urls
from project.urls import urlpatterns as project_urls
from solution.urls import urlpatterns as solution_urls
from accounts.urls import urlpatterns as account_urls
from category.urls import urlpatterns as category_urls
from supplier.urls import urlpatterns as supplier_urls
from company_info.urls import urlpatterns as company_urls
from working_field.urls import urlpatterns as working_urls
from address.urls import countries_urlpatterns as country_urls
from address.urls import states_urlpatterns as state_urls
from address.urls import cities_urlpatterns as city_urls
from address.urls import areas_urlpatterns as area_urls
from slider.urls import urlpatterns as slider_urls
from brochures.urls import urlpatterns as brochure_urls
from sellingPoint.urls import urlpatterns as selling_urls
from sms_notifications.urls import urlpatterns as sms_urls
from project_application.urls import urlpatterns as application_urls
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
from address import views as address_views
from dashboard import views as dashboard_views
from sms_notifications import views as sms_notifications_views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
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
router.register(r'address/modifyCountry', address_views.CountryViewSet, basename='CreateCountry')
router.register(r'address/modifyState', address_views.StateViewSet, basename='CreateState')
router.register(r'address/modifyCity', address_views.CityViewSet, basename='CreateCity')
router.register(r'address/modifyArea', address_views.AreaViewSet, basename='CreateArea')
router.register(r'category', category_views.CategoryViewSet, basename='CreateCategory')
router.register(r'slider', slider_views.SliderViewSet, basename='CreateSlider')
router.register(r'product/modifyProduct', product_views.ProductViewSet, basename='CreateProduct')
router.register(r'product/productImage', product_views.ProductImagesViewSet, basename='CreateProductImage')
router.register(r'product/productVideo', product_views.ProductVideoViewSet, basename='CreateProductVideo')
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
    path('', include(router.urls)),
    path('admin_panel/', include(admin_router.urls)),
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/login', dashboard_views.LoginView.as_view(), name='login'),
    path('dashboard/logout', dashboard_views.logout_view, name='logout_user'),
    path('dashboard/products/', include(product_urls)),
    path('dashboard/projects/', include(project_urls)),
    path('dashboard/solutions/', include(solution_urls)),
    path('dashboard/categories/', include(category_urls)),
    path('dashboard/users/', include(account_urls)),
    path('dashboard/suppliers/', include(supplier_urls)),
    path('dashboard/countries/', include(country_urls)),
    path('dashboard/states/', include(state_urls)),
    path('dashboard/areas/', include(area_urls)),
    path('dashboard/cities/', include(city_urls)),
    path('dashboard/sliders/', include(slider_urls)),
    path('dashboard/sellingPoints/', include(selling_urls)),
    path('dashboard/brochures/', include(brochure_urls)),
    path('dashboard/SMSs/', include(sms_urls)),
    path('dashboard/CompanyInfo/', include(company_urls)),
    path('dashboard/ProjectApplications/', include(application_urls)),
    path('dashboard/workingField/', include(working_urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('logout/', accounts_views.Logout.as_view(), name='logout'),
    # re_path('^product/(?P<category_id>.+)/$',product_views.FetchProductsByCategoryViewSet,name='FetchProduct'),
    # re_path('product/(?P[0-9][,].+)/$',product_views.FetchProductsByCategoryViewSet.as_view(),name='FetchProducts'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('dashboard/images/favicon.ico'))),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
