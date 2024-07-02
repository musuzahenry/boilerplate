from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from sysadmin.models import Employee, Position
from hr.forms import EmployeeForm
from django.contrib import messages


class EmployeeListView(ListView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texter"] = "you are tested"
        context["count"] = self.get_queryset().count()
        return context

    template_name = 'hr/employee_list.html'





class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    
    template_name = 'hr/create_employee.html'
    success_message = "Your item was successfully created!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        positions = Position.objects.all()
        self.success_message = "Your item was successfully created!"
        context["positions"] = positions
        return context

    def get_success_url(self):   
        return  reverse("hr:employee-list")





class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    success_message = "Sucess, record updated"

    template_name = "hr/employee_update.html"

    def get_success_url(self):   
         return '/hr/update-employee/{}'.format(self.object.pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = self.object
        return context



class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'hr/employee_detail.html'  # Specify your template
