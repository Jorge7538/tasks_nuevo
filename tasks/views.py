from django.views.generic import ListView
from .models import Task

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'tasks_list.html'