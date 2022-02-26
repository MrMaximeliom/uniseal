from django.urls import path, include
from apps.accounts.urls import urlpatterns as account_urls
from apps.address.urls import areas_urlpatterns as area_urls ,\
    cities_urlpatterns as city_urls ,  countries_urlpatterns as country_urls,\
    states_urlpatterns as state_urls
from apps.application_videos.urls import urlpatterns as product_application_videos
from apps.brochures.urls import urlpatterns as brochure_urls
from apps.category.urls import urlpatterns as category_urls
from apps.company_info.urls import urlpatterns as company_urls
from apps.dashboard import views as dashboard_views
from apps.industry_updates.urls import urlpatterns as update_urls
from apps.notifications.urls import urlpatterns as notifications_urls
from apps.product.urls import urlpatterns as product_urls
from apps.project.urls import urlpatterns as project_urls
from apps.project_application.urls import urlpatterns as application_urls
from apps.sellingPoint.urls import urlpatterns as selling_urls
from apps.slider.urls import urlpatterns as slider_urls
from apps.sms_notifications.urls import urlpatterns as sms_urls
from apps.solution.urls import urlpatterns as solution_urls
from apps.supplier.urls import urlpatterns as supplier_urls
from apps.orders.urls import urlpatterns as orders_urls
from apps.jop_type.urls import urlpatterns as job_type_urls
from apps.offer.urls import urlpatterns as offers_urls
from apps.request_permissions.urls import urlpatterns as request_urls
from apps.admin_panel.urls import urlpatterns as admin_urls
from apps.approvals.urls import urlpatterns as approvals_urls
from django.contrib.auth import views as auth_views
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
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset_form.html"),name='password_reset'),
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
    path('ApplicationVideos/',include(product_application_videos)),
    path('Orders/',include(orders_urls)),
    path('JobTypes/', include(job_type_urls)),
    path('Offers/', include(offers_urls)),
    path('RequestAccess/', include(request_urls)),
    path('AdminPanel/', include(admin_urls)),
    path('Approvals/', include(approvals_urls))
]