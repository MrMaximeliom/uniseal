from django.utils.translation import gettext_lazy as _

# general for all search pages
EMPTY_SEARCH_PHRASE = _("Please enter a search phrase and select search by!")
# used by account search pages
USERNAME_SYNTAX_ERROR = _("Username contains alphanumeric English letters only!")
FULL_NAME_SYNTAX_ERROR = _("Full Name contains English letters only!")
ORGANIZATION_NAME_SYNTAX_ERROR = _("Organization Name contains only English letters!")
PHONE_NUMBER_SYNTAX_ERROR = _("Phone Number contains only numbers! , in the format of 09###### or 01######")
# used by product search pages
PRODUCT_NAME_SYNTAX_ERROR = _("Product name contains alphanumeric English letters with dashes only!")
# used also by category pages
CATEGORY_NAME_SYNTAX_ERROR = _("Category name contains alphanumeric English letters only!")
SUPPLIER_NAME_SYNTAX_ERROR = _("Supplier name contains alphanumeric English letters only!")
# used by project search pages
PROJECT_NAME_SYNTAX_ERROR = _("Project name contains alphanumeric English letters with dashes only!")
BENEFICIARY_NAME_SYNTAX_ERROR = _("Beneficiary name contains alphanumeric English letters with dashes only!")
MAIN_MATERIAL_SYNTAX_ERROR = _("Main material name contains alphanumeric English letters with dashes only!")
PROJECT_TYPE_SYNTAX_ERROR = _("Project type name contains alphanumeric English letters with dashes only!")
EXECUTION_DATE_ERROR = _("Please choose project's execution date")
# used by project type pages
PROJECT_APPLICATION_NAME_SYNTAX_ERROR = _("Project type name contains alphanumeric English letters with dashes only!")
# used by country pages
COUNTRY_NAME_SYNTAX_ERROR = _("Country name contains alphanumeric English letters only!")
# used by state pages
STATE_NAME_SYNTAX_ERROR = _("State name contains alphanumeric English letters only!")
# used by city pages
CITY_NAME_SYNTAX_ERROR = _("City name contains alphanumeric English letters only!")
# used by city pages
AREA_NAME_SYNTAX_ERROR = _("Area name contains alphanumeric English letters only!")
# used by selling point pages
POINT_NAME_SYNTAX_ERROR = _("Selling point name contains alphanumeric English letters only!")
# Not found errors
PRODUCT_NOT_FOUND = _("Sorry no products found that matches your search!")
# Not found errors
PROJECT_NOT_FOUND = _("Sorry no projects found that matches your search!")