from django.contrib import admin
from .models import ProductImages,Product,ProductVideos,SimilarProduct
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(ProductVideos)
admin.site.register(SimilarProduct)