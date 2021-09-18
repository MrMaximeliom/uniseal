from django.urls import path

from address import area_dashboard_views as area_dashboard_views
from address import city_dashboard_views as city_dashboard_views
from address import country_dashboard_views as country_dashboard_views
from address import state_dashboard_views as state_dashboard_views

countries_urlpatterns = [
     path('allCountries', country_dashboard_views.all_countries, name='allCountries'),
    path('addCountries', country_dashboard_views.add_countries, name='addCountries'),
    path('deleteCountries', country_dashboard_views.delete_countries, name='deleteCountries'),
    path('editCountries', country_dashboard_views.edit_countries, name='editCountries'),
    path('editCountries/<str:slug>', country_dashboard_views.edit_country, name='editCountry'),
    path('deleteCountry/<int:id>', country_dashboard_views.confirm_country_delete, name='deleteCountry'),
    ]
states_urlpatterns = [
    path('allStates', state_dashboard_views.all_states, name='allStates'),
    path('addStates', state_dashboard_views.add_states, name='addStates'),
    path('deleteStates', state_dashboard_views.delete_states, name='deleteStates'),
    path('editStates', state_dashboard_views.edit_states, name='editStates'),
    path('editStates/<str:slug>', state_dashboard_views.edit_state, name='editState'),
    path('deleteState/<int:id>', state_dashboard_views.confirm_state_delete, name='deleteState'),
]
cities_urlpatterns = [
    path('allCities', city_dashboard_views.all_cities, name='allCities'),
    path('addCities', city_dashboard_views.add_cities, name='addCities'),
    path('deleteCities', city_dashboard_views.delete_cities, name='deleteCities'),
    path('editCities', city_dashboard_views.edit_cities, name='editCities'),
    path('editCity/<str:slug>', city_dashboard_views.edit_city, name='editCity'),
    path('deleteCity/<int:id>', city_dashboard_views.confirm_city_delete, name='deleteCity'),
]
areas_urlpatterns = [
path('allAreas', area_dashboard_views.all_areas, name='allAreas'),
    path('addAreas', area_dashboard_views.add_areas, name='addAreas'),
    path('deleteAreas', area_dashboard_views.delete_areas, name='deleteAreas'),
    path('editAreas', area_dashboard_views.edit_areas, name='editAreas'),
    path('editArea/<str:slug>', area_dashboard_views.edit_area, name='editArea'),
    path('deleteArea/<int:id>', area_dashboard_views.confirm_area_delete, name='deleteArea'),
]