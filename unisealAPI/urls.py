from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from uniseal import views as uniseal_views
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'supplier', uniseal_views.SupplierViewSet,basename='CreateSupplier')
router.register(r'product', uniseal_views.ProductViewSet,basename='CreateProduct')
router.register(r'productImage', uniseal_views.ProductViewSet,basename='CreateProductImage')
router.register(r'productVideo', uniseal_views.ProductVideoViewSet,basename='CreateProductVideo')
router.register(r'similarProduct', uniseal_views.SimilarProductViewSet,basename='LinkSimilarProducts')
router.register(r'project', uniseal_views.ProjectViewSet,basename='CreateProject')
router.register(r'projectImage', uniseal_views.ProjectImagesViewSet,basename='CreateProjectImages')
router.register(r'projectVideo', uniseal_views.ProjectVideoViewSet,basename='CreateProjectVideo')
router.register(r'sellingPoint', uniseal_views.SellingPointViewSet,basename='CreateSellingPoint')





urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)