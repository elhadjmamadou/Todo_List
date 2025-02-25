from django.urls import path, include
from .views import ExportTasksCSVView, HomeView, ImportTasksCSVView, signUp, profile, TaskCreateView, TaskListView,TaskUpdateView,TaskDeleteView,TaskDetailView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', HomeView, name='home'),  # Page d'accueil
    path('compte/nouveau/', signUp, name='signup'),
    path('accounts/profile/', profile, name='profile'),
    path('compte/logout/', LogoutView.as_view(), name='logout'),  # URL de déconnexion
    path('compte/', include("django.contrib.auth.urls")),
    
    path('list/', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='edit_task'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
    
    path('import/csv/', ImportTasksCSVView.as_view(), name='import_tasks_csv'),
    path('export/csv/', ExportTasksCSVView.as_view(), name='export_tasks_csv'),
    
    path('tache/<int:pk>/', TaskDetailView.as_view(), name='task_detail'), 
]
