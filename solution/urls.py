from django.urls import path
from solution import views as solution_views
urlpatterns = [
    path('allSolutions', solution_views.all_solutions, name='allSolutions'),
    path('addSolutions', solution_views.add_solutions, name='addSolutions'),
    path('deleteSolutions', solution_views.delete_solutions, name='deleteSolutions'),
    path('editSolutions', solution_views.edit_solutions, name='editSolutions'),
    ]