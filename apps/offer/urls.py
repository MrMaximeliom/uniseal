from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from Util.search_form_strings import DELETE_OFFERS_TITLE, EDIT_OFFERS_TITLE
from apps.common_code.views import ModelDeleteView
from apps.offer import dashboard_views as offer_views
from apps.offer.models import Offer

urlpatterns = [
    path('allOffers', offer_views.OffersListView.as_view(), name='offersList'),
    path('addOffers', offer_views.OfferFormView.as_view(), name='addOffers'),
    path('editOffers', offer_views.OffersListView.as_view(template_name ="offer/edit_offers.html", active_flag="edit_offers",title=EDIT_OFFERS_TITLE), name='editOffers'),
    path('editOffer/<str:slug>/', offer_views.OfferUpdateView.as_view(), name='editOffer'),
    path('deleteOffers', offer_views.OffersListView.as_view(template_name ="offer/delete_offers.html", active_flag="delete_offers",title=DELETE_OFFERS_TITLE), name='deleteOffers'),
    path('deleteOffer/<str:slug>/', staff_member_required(ModelDeleteView.as_view(
        model=Offer,
        main_active_flag="offers",
        active_flag="delete_offers",
        model_name='Offer',
        title="Delete Offers",
        success_url="allOffers"
    ), login_url="login"), name="deleteOffer"),
]