from django.urls import path
from address import views as address_views
countries_urlpatterns = [
     path('allCountries', address_views.all_countries, name='allCountries'),
    path('addCountries', address_views.add_countries, name='addCountries'),
    path('deleteCountries', address_views.delete_countries, name='deleteCountries'),
    path('editCountries', address_views.edit_countries, name='editCountries'),
    path('editCountries/<str:slug>', address_views.edit_country, name='editCountry'),
    path('deleteCountry/<int:id>', address_views.confirm_country_delete, name='deleteCountry'),
    ]
states_urlpatterns = [
    path('allStates', address_views.all_states, name='allStates'),
    path('addStates', address_views.add_states, name='addStates'),
    path('deleteStates', address_views.delete_states, name='deleteStates'),
    path('editStates', address_views.edit_states, name='editStates'),
    path('editStates/<str:slug>', address_views.edit_state, name='editState'),
    path('deleteState/<int:id>', address_views.confirm_state_delete, name='deleteState'),
]
cities_urlpatterns = [
    path('allCities', address_views.all_cities, name='allCities'),
    path('addCities', address_views.add_cities, name='addCities'),
    path('deleteCities', address_views.delete_cities, name='deleteCities'),
    path('editCities', address_views.edit_cities, name='editCities'),
    path('editCity/<str:slug>', address_views.edit_city, name='editCity'),
    path('deleteCity/<int:id>', address_views.confirm_city_delete, name='deleteCity'),
]
areas_urlpatterns = [
path('allAreas', address_views.all_areas, name='allAreas'),
    path('addAreas', address_views.add_areas, name='addAreas'),
    path('deleteAreas', address_views.delete_areas, name='deleteAreas'),
    path('editAreas', address_views.edit_areas, name='editAreas'),
    path('editArea/<str:slug>', address_views.edit_area, name='editArea'),
    path('deleteArea/<int:id>', address_views.confirm_area_delete, name='deleteArea'),
]