from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.address.area_dashboard_views import AreaListView
from apps.address.city_dashboard_views import CityListView
from apps.address.country_dashboard_views import CountryListView
from apps.address.models import Country, State, City, Area
from apps.address.state_dashboard_views import StateListView
from apps.common_code.views import AddModelView, UpdateModelView, ModelDeleteView

countries_urlpatterns = [
    path('allCountries', staff_member_required(CountryListView.as_view(
        model=Country,
        template_name="address/all_countries.html",
        main_active_flag="address",
        active_flag="all_countries",
        model_name="Country",
        title="All Countries"
    ), login_url="login"), name="allCountries"),
    path('addCountries', staff_member_required(AddModelView.as_view(
        model=Country,
        fields=['name'],
        main_active_flag="address",
        active_flag="add_countries",
        reference_field_name="name",
        template_name="address/add_countries.html",
        title="Add Countries",
        success_url="addCountries"
    ), login_url="login"), name="addCountries"),
    path('deleteCountries', staff_member_required(CountryListView.as_view(
        model=Country,
        template_name="address/delete_countries.html",
        main_active_flag="address",
        active_flag="delete_countries",
        model_name="Country",
        title="Delete Countries"
    ), login_url="login"), name="deleteCountries"),
    path('deleteCountry/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Country,
        main_active_flag="address",
        active_flag="delete_countries",
        model_name='country',
        title="Delete Countries",
        success_url="deleteCountries"
    ), login_url="login"), name="deleteCountry"),
    path('editCountries', staff_member_required(CountryListView.as_view(
        model=Country,
        template_name="address/edit_countries.html",
        main_active_flag="address",
        active_flag="edit_countries",
        model_name="Country",
        title="Update Countries"
    ), login_url="login"), name="editCountries"),
    path('editCountry/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=Country,
        fields=['name'],
        active_flag="edit_countries",
        main_active_flag="address",
        reference_field_name="name",
        template_name="address/edit_country.html",
        title="Update Country",
        success_url="editCountries"
    ), login_url="login"), name="editCountry"),
    ]
states_urlpatterns = [
    path('allStates', staff_member_required(StateListView.as_view(
        model=State,
        template_name="address/all_states.html",
        main_active_flag="address",
        active_flag="all_states",
        model_name="State",
        title="All States"
    ), login_url="login"), name="allStates"),
    path('addStates', staff_member_required(AddModelView.as_view(
        model=State,
        fields=['name','country'],
        main_active_flag="address",
        active_flag="add_states",
        reference_field_name="name",
        template_name="address/add_states.html",
        title="Add States",
        success_url="addStates"
    ), login_url="login"), name="addStates"),
    path('deleteStates', staff_member_required(StateListView.as_view(
        model=State,
        template_name="address/delete_states.html",
        main_active_flag="address",
        active_flag="delete_states",
        model_name="State",
        title="Delete States"
    ), login_url="login"), name="deleteStates"),
    path('deleteState/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=State,
        main_active_flag="address",
        active_flag="delete_states",
        model_name='state',
        title="Delete States",
        success_url="deleteStates"
    ), login_url="login"), name="deleteState"),
    path('editStates', staff_member_required(StateListView.as_view(
        model=State,
        template_name="address/edit_states.html",
        main_active_flag="address",
        active_flag="edit_states",
        model_name="State",
        title="Update States"
    ), login_url="login"), name="editStates"),
    path('editState/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=State,
        fields=['name','country'],
        active_flag="edit_states",
        main_active_flag="address",
        reference_field_name="name",
        template_name="address/edit_state.html",
        title="Update State",
        success_url="editStates"
    ), login_url="login"), name="editState"),
]
cities_urlpatterns = [
    path('allCities', staff_member_required(CityListView.as_view(
        model=City,
        template_name="address/all_cities.html",
        main_active_flag="address",
        active_flag="all_cities",
        model_name="City",
        title="All Cities"
    ), login_url="login"), name="allCities"),
    path('addCities', staff_member_required(AddModelView.as_view(
        model=City,
        fields=['name','state'],
        main_active_flag="address",
        active_flag="add_cities",
        reference_field_name="name",
        template_name="address/add_cities.html",
        title="Add Cities",
        success_url="addCities"
    ), login_url="login"), name="addCities"),
    path('deleteCities', staff_member_required(CityListView.as_view(
        model=City,
        template_name="address/delete_cities.html",
        main_active_flag="address",
        active_flag="delete_cities",
        model_name="City",
        title="Delete Cities"
    ), login_url="login"), name="deleteCities"),
    path('deleteCity/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=City,
        main_active_flag="address",
        active_flag="delete_cities",
        model_name='City',
        title="Delete Cities",
        success_url="deleteCities"
    ), login_url="login"), name="deleteCity"),
    path('editCities', staff_member_required(CityListView.as_view(
        model=City,
        template_name="address/edit_cities.html",
        main_active_flag="address",
        active_flag="edit_cities",
        model_name="City",
        title="Update Cities"
    ), login_url="login"), name="editCities"),
    path('editCity/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=City,
        fields=['name', 'state'],
        active_flag="edit_cities",
        main_active_flag="address",
        reference_field_name="name",
        template_name="address/edit_city.html",
        title="Update City",
        success_url="editCities"
    ), login_url="login"), name="editCity"),

]
areas_urlpatterns = [
    path('allAreas', staff_member_required(AreaListView.as_view(
        model=Area,
        template_name="address/all_areas.html",
        main_active_flag="address",
        active_flag="all_areas",
        model_name="Area",
        title="All Areas"
    ), login_url="login"), name="allAreas"),
    path('addAreas', staff_member_required(AddModelView.as_view(
        model=Area,
        fields=['name', 'city'],
        main_active_flag="address",
        active_flag="add_areas",
        reference_field_name="name",
        template_name="address/add_areas.html",
        title="Add Areas",
        success_url="allAreas"
    ), login_url="login"), name="addAreas"),
    path('deleteAreas', staff_member_required(CityListView.as_view(
        model=Area,
        template_name="address/delete_areas.html",
        main_active_flag="address",
        active_flag="delete_areas",
        model_name="Area",
        title="Delete Areas"
    ), login_url="login"), name="deleteAreas"),
    path('deleteArea/<slug:slug>', staff_member_required(ModelDeleteView.as_view(
        model=Area,
        main_active_flag="address",
        active_flag="delete_areas",
        model_name='Area',
        title="Delete Areas",
        success_url="deleteAreas"
    ), login_url="login"), name="deleteArea"),
    path('editAreas', staff_member_required(AreaListView.as_view(
        model=Area,
        template_name="address/edit_areas.html",
        main_active_flag="address",
        active_flag="edit_areas",
        model_name="Area",
        title="Update Areas"
    ), login_url="login"), name="editAreas"),
    path('editArea/<slug:slug>', staff_member_required(UpdateModelView.as_view(
        model=Area,
        fields=['name', 'city'],
        active_flag="edit_areas",
        main_active_flag="address",
        reference_field_name="name",
        template_name="address/edit_area.html",
        title="Update Area",
        success_url="editAreas"
    ), login_url="login"), name="editArea"),

]