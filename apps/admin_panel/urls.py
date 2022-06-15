from django.urls import path

from apps.admin_panel import dashboard_views as admin_panel_views

urlpatterns = [
    path('allProductsViews', admin_panel_views.ViewsReportsListView.as_view(), name='productsViews'),
    path('allProductsPageViews', admin_panel_views.ProductsPageViews.as_view(), name='productsPageViews'),
    path('allProjectsViews', admin_panel_views.ProjectsViewsListView.as_view(), name='projectsViews'),
    path('allSolutionsViews', admin_panel_views.SolutionsViewsListView.as_view(), name='solutionsViews'),
    path('allSellingPointsViews', admin_panel_views.SellingPointsViewsListView.as_view(), name='sellingPointsViews'),
    path('allBrochuresViews', admin_panel_views.BrochuresViewsListView.as_view(), name='brochuresViews'),
    path('allOrdersViews', admin_panel_views.OrdersViewsListView.as_view(), name='ordersViews'),

]