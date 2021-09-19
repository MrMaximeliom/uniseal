from django.urls import path, include

from accounts.urls import urlpatterns as account_urls
from address.urls import areas_urlpatterns as area_urls
from address.urls import cities_urlpatterns as city_urls
from address.urls import countries_urlpatterns as country_urls
from address.urls import states_urlpatterns as state_urls
from application_videos.urls import urlpatterns as product_application_videos
from brochures.urls import urlpatterns as brochure_urls
from category.urls import urlpatterns as category_urls
from company_info.urls import urlpatterns as company_urls
from dashboard import views as dashboard_views
from industry_updates.urls import urlpatterns as update_urls
from notifications.urls import urlpatterns as notifications_urls
from product.urls import urlpatterns as product_urls
from project.urls import urlpatterns as project_urls
from project_application.urls import urlpatterns as application_urls
from sellingPoint.urls import urlpatterns as selling_urls
from slider.urls import urlpatterns as slider_urls
from sms_notifications.urls import urlpatterns as sms_urls
from solution.urls import urlpatterns as solution_urls
from supplier.urls import urlpatterns as supplier_urls

urlpatterns = [
    path('home/', dashboard_views.dashboard, name='dashboard'),
    path('product-categories-chart/', dashboard_views.products_categories_chart, name='product-categories-chart'),
    path('users-count-month-chart/', dashboard_views.users_registration_count_each_month_chart, name='users-count-month-chart'),
    path('login', dashboard_views.LoginView.as_view(), name='login'),
    path('logout', dashboard_views.logout_view, name='logout_user'),
    path('products/', include(product_urls)),
    path('projects/', include(project_urls)),
    path('solutions/', include(solution_urls)),
    path('categories/', include(category_urls)),
    path('users/', include(account_urls)),
    path('suppliers/', include(supplier_urls)),
    path('countries/', include(country_urls)),
    path('states/', include(state_urls)),
    path('areas/', include(area_urls)),
    path('cities/', include(city_urls)),
    path('sliders/', include(slider_urls)),
    path('sellingPoints/', include(selling_urls)),
    path('brochures/', include(brochure_urls)),
    path('SMSs/', include(sms_urls)),
    path('CompanyInfo/', include(company_urls)),
    path('ProjectApplications/', include(application_urls)),
    path('IndustryUpdates/', include(update_urls)),
    path('Notifications/', include(notifications_urls)),
    path('applicationVideos/',include(product_application_videos))


]