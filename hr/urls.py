

from django.urls import path
from  hr . views import *



urlpatterns =[
    #user view urls
    path("", Index.index_views, name="index"),
    path("employee-list", EmployeeListView.as_view(), name="employee-list"),
    path("create-employee", EmployeeCreateView.as_view(), name="create-employee"),
    path("update-employee/<int:pk>", EmployeeUpdateView.as_view(), name="update-employee"),
    path("employee-details/<int:pk>", EmployeeDetailView.as_view(), name = "employee-details"),
    path("make-emp-payments", EmployeeViews.make_emp_payments, name= "make-emp-payments"),
    path("employee-payments", EmployeeViews.employee_payments, name= "employee-payments"),
    path("delete-employee/<int:id>", EmployeeViews.delete_employee, name = "delete-employee"),
    path("deleted-employees", EmployeeViews.deleted_employees, name="deleted-employees"),
    path("restore-employee/<int:id>", EmployeeViews.restore_employee, name="restore-employee"),
]