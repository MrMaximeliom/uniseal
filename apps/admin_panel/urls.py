from django.urls import path

from apps.admin_panel import dashboard_views as admin_panel_views
# from Util.search_form_strings import DELETE_OFFERS_TITLE,EDIT_OFFERS_TITLE

urlpatterns = [
    path('allProductsViews', admin_panel_views.ViewsReportsListView.as_view(), name='productsViews'),
    path('allProductsPageViews', admin_panel_views.ProductsPageViews.as_view(), name='productsPageViews'),
    path('allProjectsViews', admin_panel_views.ProjectsViewsListView.as_view(), name='projectsViews'),
    path('allSolutionsViews', admin_panel_views.SolutionsViewsListView.as_view(), name='solutionsViews'),
    path('allSellingPointsViews', admin_panel_views.SellingPointsViewsListView.as_view(), name='sellingPointsViews'),
    path('allBrochuresViews', admin_panel_views.BrochuresViewsListView.as_view(), name='brochuresViews'),
    path('allOrdersViews', admin_panel_views.OrdersViewsListView.as_view(), name='ordersViews'),
    # path('addOffers', offer_views.OfferFormView.as_view(), name='addOffers'),
    # path('editOffers', offer_views.OffersListView.as_view(template_name ="offer/edit_offers.html", active_flag="edit_offers",title=EDIT_OFFERS_TITLE), name='editOffers'),
    # path('editOffer/<str:slug>/', offer_views.OfferUpdateView.as_view(), name='editOffer'),
    # path('deleteOffers', offer_views.OffersListView.as_view(template_name ="offer/delete_offers.html", active_flag="delete_offers",title=DELETE_OFFERS_TITLE), name='deleteOffers'),
    # path('deleteOffer/<str:slug>/', offer_views.confirm_delete, name='deleteOffer'),
]