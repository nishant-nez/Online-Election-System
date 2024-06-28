from django.urls import path
from . import views

urlpatterns = [
    # dashboard
    path('', views.dashboard, name='admin-dashboard'),
    # elections
    path('elections/', views.elections, name='admin-elections'),
    path('elections/create/', views.election_form, name='election-form'),
    path('elections/delete/<int:pk>/', views.confirm_election_delete, name='confirm_election_delete'),
    path('elections/update/<int:pk>/', views.election_update_form, name='election_update_form'),
    # candidates
    path('candidates/', views.candidates, name='admin_candidates'),
    path('candidates/create/', views.candidate_form, name='candidate_form'),
    path('candidates/delete/<int:pk>/', views.confirm_candidate_delete, name='confirm_candidate_delete'),
    path('candidates/update/<int:pk>/', views.candidate_update_form, name='candidate_update_form'),
    # voters
    path('voters/', views.voters, name='admin_voters'),
    path('voters/delete/<int:pk>/', views.confirm_voter_delete, name='confirm_voter_delete'),
    # results
    path('results/', views.results, name='admin_results'),
    path('results/create/<int:pk>/', views.confirm_result, name='confirm_result'),
    path('results/update/<int:pk>/', views.result_update_form, name='result_update_form'),
]
