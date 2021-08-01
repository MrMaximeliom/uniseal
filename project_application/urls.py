from django.urls import path
from project_application import views as project_views
urlpatterns = [
    path('allSolutions', solution_views.all_solutions, name='allSolutions'),
  ]