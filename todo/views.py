from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Todo

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterView, self).get(*args, **kwargs)

class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = 'todos'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = context['todos'].filter(user=self.request.user)
        context['count'] = context['todos'].filter(completed=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['todos'] = context['todos'].filter(title__startswith=search_input)
        context['search_input'] = search_input
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'completed']
    template_name = 'create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreateView, self).form_valid(form)

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields  = ['title', 'description', 'completed']
    context_object_name = 'todo'
    template_name = 'update.html'
    success_url = reverse_lazy('home')

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    context_object_name = 'todo'
    template_name = 'delete.html'
    success_url = reverse_lazy('home')
