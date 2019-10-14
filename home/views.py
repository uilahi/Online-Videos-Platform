from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.views import generic
from .models import Page, Video

def home(request):
    return render(request, 'home/home.html')

def dashboard(request):
    return render(request, 'home/dashboard.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get("username"), form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreatePage(generic.CreateView):
    model = Page
    fields = ['title']
    template_name = 'home/create_page.html'
    success_url = reverse_lazy('dashboard')


    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreatePage, self).form_valid(form)
        return redirect('home')


class DetailPage(generic.DeleteView):
    model = Page
    template_name = 'home/detail_page.html'


class UpdatePage(generic.UpdateView):
    model = Page
    template_name = 'home/update_page.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')


class DeletePage(generic.DeleteView):
    model = Page
    template_name = 'home/delete_page.html'
    success_url = reverse_lazy('dashboard')
