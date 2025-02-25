from django.shortcuts import redirect, render
from django.views import View
from .forms import ImportTasksForm, UseregistrationForm
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView

import csv
import io
from django.views.generic.edit import FormView
from django.contrib import messages





def HomeView(request):
    return render(request,"accounts/home.html")


def signUp(request):
    if request.method == "POST":
        form = UseregistrationForm(request._post)
        if form.is_valid:
            form.save()
            return redirect("home")
    else:
        form = UseregistrationForm()
    return render(request, 'accounts/signup.html', {"form":form})


def profile(request):
    # Utilisation de guillemets triples pour éviter les conflits
    response_content = f"""
        <h1>Bienvenue</h1>
        <h2>{request.user.email}</h2>
        <h2>{request.user.Nom}</h2>
        <h2>{request.user.Prenom}</h2>
        <a href="{reverse('task_list')}">Suivant</a>
    """
    return HttpResponse(response_content)
class TaskDetailView(DetailView):
    model = Task
    template_name = 'accounts/task_detail.html'  # Le template pour afficher les détails de la tâche
    context_object_name = 'task'

# class TaskCreateView(LoginRequiredMixin, CreateView):
#     model = Task
#     form_class = TaskForm
#     template_name = 'accounts/create_task.html'
#     success_url = reverse_lazy('task_list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user  # Associe la tâche à l'utilisateur connecté
#         return super().form_valid(form)

class TaskListView(ListView):
    model = Task
    template_name = 'accounts/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        priority = self.request.GET.get('priority')
        due_date = self.request.GET.get('due_date')
        
        if priority:
            queryset = queryset.filter(priority=priority)
        
        if due_date:
            queryset = queryset.filter(due_date=due_date)
        
        return queryset




# class TaskUpdateView(UpdateView):
#     model = Task
#     form_class = TaskForm
#     template_name = 'accounts/update_task.html'
#     success_url = reverse_lazy('task_list')

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user=self.request.user)


# class TaskDeleteView(DeleteView):
#     model = Task
#     template_name = 'accounts/delete_task.html'
#     success_url = reverse_lazy('task_list')

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user=self.request.user)



def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class TaskCreateView(CreateView,LoginRequiredMixin):
    model = Task
    form_class = TaskForm
    template_name = 'accounts/create_task.html'
    success_url = reverse_lazy('task_list')
    def form_valid(self, form):
        form.instance.user = self.request.user  # Associe l'utilisateur connecté à la tâche
        return super().form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'accounts/update_task.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'accounts/delete_task.html'
    success_url = reverse_lazy('task_list')


class ImportTasksCSVView(FormView):
    template_name = 'accounts/import_tasks.html'
    form_class = ImportTasksForm

    def form_valid(self, form):
        csv_file = form.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(self.request, 'Le fichier doit être au format CSV.')
            return self.form_invalid(form)

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        reader = csv.reader(io_string)
        next(reader)  # Skip the header row
        for row in reader:
            _, created = Task.objects.get_or_create(
                title=row[1],
                description=row[2],
                due_date=row[3],
                priority=row[4],
                completed=row[5],
                category=row[6]
            )
        messages.success(self.request, 'Les tâches ont été importées avec succès.')
        return redirect('task_list')



class ExportTasksCSVView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Titre', 'Description', 'Date d’échéance', 'Priorité', 'Complétée', 'Catégorie'])

        tasks = Task.objects.all()
        for task in tasks:
            writer.writerow([
                task.id,
                task.title,
                task.description,
                task.due_date,
                task.priority,
                task.completed,
                task.category
            ])

        return response
