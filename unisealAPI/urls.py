from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounts import views as accounts_views
from supplier import views as supplier_views
from slider import views as slider_views
from category import views as category_views
from product import views as product_views
from project import views as project_views
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
router.register(r'sellingPoint/createSellingPoint', selling_point_views.SellingPointViewSet,
                basename='CreateSellingPoint')
router.register(r'brochures', brochures_views.BrochuresViewSet, basename='CreateBrochures')
router.register(r'contactUs', accounts_views.ContactUsViewSet, basename='CreateContactUsMessage')
router.register(r'solution/createSolution', solution_views.SolutionViewSet, basename='CreateSolution')
router.register(r'solution/solutionImages', solution_views.SolutionImagesViewSet, basename='CreateSolutionImages')
router.register(r'solution/solutionVideos', solution_views.SolutionVideosViewSet, basename='CreateSolutionVideo')
admin_router.register(r'manageProducts', admin_views.ManageProductsViewSet, basename='ManageProducts')
admin_router.register(r'manageProjects', admin_views.ManageProjectsViewSet, basename='ManageProjects')
admin_router.register(r'manageSolution', admin_views.ManageSolutionViewSet, basename='ManageSolution')
admin_router.register(r'manageSellingPoints', admin_views.ManageSellingPointsViewSet, basename='ManageSellingPoints')
admin_router.register(r'manageBrochures', admin_views.ManageBrochuresViewSet, basename='MManageBrochures')

urlpatterns = [
    path('', include(router.urls)),
    path('admin_panel/', include(admin_router.urls)),
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard_views.dashboard,name='dashboard'),
    path('dashboard/allProducts', product_views.all_products,name='allProducts'),
    path('dashboard/addProducts', product_views.add_products,name='addProducts'),
    path('dashboard/deleteProducts', product_views.delete_products,name='deleteProducts'),
    path('dashboard/editProducts', product_views.edit_products,name='editProducts'),
    path('dashboard/allProjects', project_views.all_projects, name='allProjects'),
    path('dashboard/addProjects', project_views.add_projects, name='addProjects'),
    path('dashboard/deleteProjects', project_views.delete_projects, name='deleteProjects'),
    path('dashboard/editProjects', project_views.edit_projects, name='editProjects'),
    path('dashboard/allSolutions', solution_views.all_solutions, name='allSolutions'),
    path('dashboard/addSolutions', solution_views.add_solutions, name='addSolutions'),
    path('dashboard/deleteSolutions', solution_views.delete_solutions, name='deleteSolutions'),
    path('dashboard/editSolutions', solution_views.edit_solutions, name='editSolutions'),
    path('dashboard/allCategories', category_views.all_categories, name='allCategories'),
    path('dashboard/addCategories', category_views.add_categories, name='addCategories'),
    path('dashboard/deleteCategories', category_views.delete_categories, name='deleteCategories'),
    path('dashboard/editCategories', category_views.edit_categories, name='editCategories'),
    path('dashboard/allUsers', accounts_views.all_users, name='allUsers'),
    path('dashboard/addUsers', accounts_views.add_users, name='addUsers'),
    path('dashboard/deleteUsers', accounts_views.delete_users, name='deleteUsers'),
    path('dashboard/editUsers', accounts_views.edit_users, name='editUsers'),
    path('dashboard/allCountries', address_views.all_countries, name='allCountries'),
    path('dashboard/addCountries', address_views.add_countries, name='addCountries'),
    path('dashboard/deleteCountries', address_views.delete_countries, name='deleteCountries'),
    path('dashboard/editCountries', address_views.edit_countries, name='editCountries'),
    path('dashboard/allStates', address_views.all_states, name='allStates'),
    path('dashboard/addStates', address_views.add_states, name='addStates'),
    path('dashboard/deleteStates', address_views.delete_states, name='deleteStates'),
    path('dashboard/editStates', address_views.edit_states, name='editStates'),
    path('dashboard/allAreas', address_views.all_areas, name='allAreas'),
    path('dashboard/addAreas', address_views.add_areas, name='addAreas'),
    path('dashboard/deleteAreas', address_views.delete_areas, name='deleteAreas'),
    path('dashboard/editAreas', address_views.edit_areas, name='editAreas'),
    path('dashboard/allCities', address_views.all_cities, name='allCities'),
    path('dashboard/addCities', address_views.add_cities, name='addCities'),
    path('dashboard/deleteCities', address_views.delete_cities, name='deleteCities'),
    path('dashboard/editCities', address_views.edit_cities, name='editCities'),
    path('dashboard/allSliders', slider_views.all_sliders, name='allSliders'),
    path('dashboard/addSliders', slider_views.add_sliders, name='addSliders'),
    path('dashboard/deleteSliders', slider_views.delete_sliders, name='deleteSliders'),
    path('dashboard/editSliders', slider_views.edit_sliders, name='editSliders'),
    path('dashboard/allSellingPoints', selling_point_views.all_selling_points, name='allSellingPoints'),
    path('dashboard/addSellingPoints', selling_point_views.add_selling_points, name='addSellingPoints'),
    path('dashboard/deleteSellingPoints', selling_point_views.delete_selling_points, name='deleteSellingPoints'),
    path('dashboard/editSellingPoints', selling_point_views.edit_selling_points, name='editSellingPoints'),
    path('dashboard/allBrochures', brochures_views.all_brochures, name='allBrochures'),
    path('dashboard/addBrochures', brochures_views.add_brochures, name='addBrochures'),
    path('dashboard/deleteBrochures', brochures_views.delete_brochures, name='deleteBrochures'),
    path('dashboard/editBrochures', brochures_views.edit_brochures, name='editBrochures'),
    path('dashboard/allSMS', sms_notifications_views.all_sms, name='allSMS'),
    path('dashboard/sendSMS', sms_notifications_views.send_sms, name='sendSMS'),
    path('dashboard/deleteSMS', sms_notifications_views.delete_sms, name='deleteSMS'),
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

