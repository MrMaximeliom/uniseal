from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from uniseal import views as uniseal_views
from accounts import views as accounts_views
from supplier import views as supplier_views
from category import views as category_views
from product import views as product_views
from project import views as project_views
from sellingPoint import views as selling_point_views
from brochures import views as brochures_views
from solution import views as solution_views
from admin_panel import views as admin_views
from django.conf import settings

router = routers.DefaultRouter()
admin_router = routers.DefaultRouter()
router.APIRootView.__name__ = 'Uniseal API'

router.register(r'accounts/signUp', accounts_views.RegisterUserViewSet, basename='CreateUser')
router.register(r'accounts/modifyUsersData', accounts_views.ModifyUserDataViewSet, basename='ModifyUser')
router.register(r'accounts/me', accounts_views.CurrentUserDataViewSet, basename='CurrentUser')
router.register(r'supplier', supplier_views.SupplierViewSet, basename='CreateSupplier')
router.register(r'category', category_views.CategoryViewSet, basename='CreateCategory')
router.register(r'product/createProduct', product_views.ProductViewSet, basename='CreateProduct')
router.register(r'product/productImage', product_views.ProductImagesViewSet, basename='CreateProductImage')
router.register(r'product/productVideo', product_views.ProductVideoViewSet, basename='CreateProductVideo')
router.register(r'product/similarProduct', product_views.SimilarProductViewSet, basename='LinkSimilarProducts')
router.register(r'project/createProject', project_views.ProjectViewSet, basename='CreateProject')
router.register(r'project/projectImage', project_views.ProjectImagesViewSet, basename='CreateProjectImages')
router.register(r'project/projectVideo', project_views.ProjectVideoViewSet, basename='CreateProjectVideo')
router.register(r'sellingPoint/createSellingPoint', selling_point_views.SellingPointViewSet,
                basename='CreateSellingPoint')
# router.register(r'sellingPoint/contactInfo', selling_point_views.SellingPointsContactInfoViewSet,
#                 basename='CreateSellingPointContactInfo')
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
    path('admin_panel/',include(admin_router.urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
