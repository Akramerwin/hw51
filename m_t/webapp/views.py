from django.shortcuts import render, reverse, redirect, get_object_or_404
from webapp.models import Todo
from webapp.forms import TodoForm
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView

class TodoView(TemplateView):
    def get(self, request, *args, **kwargs):
       template_name = 'index.html'
       todo = Todo.objects.all()
       context = {
           'todo': todo
       }
       return render(request, template_name, context)


class View(TemplateView):
   template_name = 'todo_view.html'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['todo'] = get_object_or_404(Todo, pk=kwargs['pk'])
       return context


class TodoCreate(FormView):
    template_name = 'todo_create.html'
    form_class = TodoForm

    def get_success_url(self):
        return reverse('view', kwargs = {'pk': self.todo.pk})

    def form_valid(self, form):
        # type = form.cleaned_data.pop('type')
        # self.todo = Todo.objects.create(**form.cleaned_data)
        # self.todo.type.set(type)
        self.todo = form.save()
        return super().form_valid(form)


class UpdateTodo(FormView):
    template_name = 'todo_update.html'
    form_class = TodoForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Todo, pk = pk)

    def dispatch(self, request, *args, **kwargs):
        self.todo = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.todo
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.todo
        return kwargs
    # def get_initial(self):
    #     initial = {}
    #     for key in 'short_description', 'description', 'status':
    #         initial[key] = getattr(self.todo, key)
    #     initial['type'] = self.todo.type.all()
    #     return initial

    def form_valid(self, form):
        # type = form.cleaned_data.pop('type')
        # for key, value in form.cleaned_data.items():
        #     if value is not None:
        #         setattr(self.todo, key, value)
        # self.todo.save()
        # self.todo.type.set(type)
        self.todo = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view', kwargs = {'pk': self.todo.pk})



class Delete(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        return render(request, 'delete.html', context={'todo': todo})
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return redirect('index')