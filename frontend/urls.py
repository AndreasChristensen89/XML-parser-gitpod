from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='index'),
    # xml creation
    path('insert-sample/', views.insert_sample, name='insert_sample'),
    path('insert-publication/', views.insert_publication, name='insert_publication'),
    path('add-experiment-intro/', views.add_experiment_intro, name='add_experiment_intro'),
    path('add-experiment-geolocation/', views.add_experiment_geolocation, name='add_geolocation'),
    path('add-experiment-parameters-instrument/', views.add_experiment_parameters_instrument, name='add_parameters_instrument'),
    path('add-experiment-multiple-sections/', views.add_experiment_multiple_sections, name='add_experiment_multiple_sections'),
    path('add-experiment-spectra/', views.add_experiment_spectra, name='add_experiment_spectra'),
    path('add-experiment-finish/', views.add_experiment_finish, name='add_experiment_finish'),
    # upload files
    path('upload-publication/', views.upload_publication_file, name='upload_publication'),
    path('upload-experiment/', views.upload_experiment_file, name='upload_experiment'),
    path('upload-sample/', views.upload_sample_file, name='upload_sample'),
    # clear data
    path('clear-publication-data/', views.clear_publication_data, name='clear_publication_data'),
    path('clear-sample-data/', views.clear_sample_data, name='clear_sample_data'),
    path('clear-experiment-data/', views.clear_experiment_data, name='clear_experiment_data'),
    # delete session
    path('delete-experiment-intro/', views.delete_experiment_intro, name='delete_experiment_intro'),
    path('delete-experiment-geolocation/', views.delete_experiment_geolocation, name='delete_experiment_geolocation'),
    path('delete-experiment-parameter-instrument/', views.delete_experiment_parameters_instrument, name='delete_experiment_parameters_instrument'),
    path('delete-experiment-multiple-sections/', views.delete_experiment_multiple_sections, name='delete_experiment_multiple_sections'),
    path('delete-experiment-spectra/', views.delete_experiment_spectra, name='delete_experiment_spectra'),
    # ad hoc
    path('contact/', views.contact, name='contact'),
    # path('insert-experiment/', views.insert_experiment, name='insert_experiment'),
]