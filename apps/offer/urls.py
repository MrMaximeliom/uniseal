from django.urls import path

from apps.offer import dashboard_views as offer_views
from Util.search_form_strings import DELETE_OFFERS_TITLE,EDIT_OFFERS_TITLE

urlpatterns = [
    path('allOffers', offer_views.OffersListView.as_view(), name='offersList'),
    path('addOffers', offer_views.OfferFormView.as_view(), name='addOffers'),
    path('editOffers', offer_views.OffersListView.as_view(template_name ="offer/edit_offers.html", active_flag="edit_offers",title=EDIT_OFFERS_TITLE), name='editOffers'),
    path('editOffer/<str:slug>/', offer_views.OfferUpdateView.as_view(), name='editOffer'),
    path('deleteOffers', offer_views.OffersListView.as_view(template_name ="offer/delete_offers.html", active_flag="delete_offers",title=DELETE_OFFERS_TITLE), name='deleteOffers'),
    path('deleteOffer/<str:slug>/', offer_views.confirm_delete, name='deleteOffer'),
]